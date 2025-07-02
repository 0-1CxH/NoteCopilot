from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import openai
import time
import yaml
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import logging

logger = logging.getLogger("AIService")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class BaseAPICompletionService(ABC):

    def __init__(self, api_endpoint, api_key, default_model_name):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.default_model_name = default_model_name
        self.supported_models = self.fetch_supported_models()
        if default_model_name not in self.supported_models:
            self.supported_models.append(default_model_name)
    
    @abstractmethod
    def __call__(
        self, 
        messages: List[Dict], 
        generation_config: dict, 
        model_name: str,
        streaming: bool
    ) -> Any:
        pass

    @abstractmethod
    def fetch_supported_models(self):
        pass

    def is_model_supported(self, model_name):
        return model_name in self.supported_models

    def generate(
        self,
        messages, #: List[Dict] | str, 
        streaming: Optional[bool],
        generation_config: Optional[dict] = None,
        model_name: Optional[str] = None,
        retry_times: int = 5,
    ):
        if model_name is None:
            model_name = self.default_model_name
        assert model_name is not None
        if isinstance(messages, str):
            messages = [
                {"role": "user", "content": messages}
            ]
        assert isinstance(messages, list)
        remaning_retry_times = retry_times
        while remaning_retry_times > 0:
            try:
                # Assuming there's a method to send a request to the API
                response = self.__call__(messages, generation_config, model_name, streaming)
                return response
            except Exception as e:
                remaning_retry_times -= 1
                backoff_time = 2 ** (2 + retry_times - remaning_retry_times)
                time.sleep(backoff_time)
                logger.error(f"An error occurred in thread worker: {e}. Retrying after {backoff_time}s... ({retry_times - remaning_retry_times + 1}/{retry_times})")
            
        # If all retries fail, return None or handle as needed
        return None

    
    def parallel_generate(
            self,
            batch_messages: List[List[Dict]], 
            generation_config: Optional[dict] = None,
            model_name: Optional[str] = None,
            parallel_size: int = 3,
            retry_times: int = 5
    ):
        if model_name is None:
            model_name = self.default_model_name
        assert model_name is not None
        def thread_worker(messages, generation_config):
            remaning_retry_times = retry_times
            while remaning_retry_times > 0:
                try:
                    # Assuming there's a method to send a request to the API
                    response = self.__call__(messages, generation_config, model_name, streaming=False)
                    return response
                except Exception as e:
                    remaning_retry_times -= 1
                    backoff_time = 2 ** (2 + retry_times - remaning_retry_times)
                    time.sleep(backoff_time)
                    logger.error(f"An error occurred in thread worker: {e}. Retrying after {backoff_time}s... ({retry_times - remaning_retry_times + 1}/{retry_times})")
                
            # If all retries fail, return None or handle as needed
            return None
        
        results = [None] * len(batch_messages)

        with ThreadPoolExecutor(max_workers=parallel_size) as executor:
            future_to_index = {
                executor.submit(thread_worker, messages, generation_config): idx
                for idx, messages in enumerate(batch_messages)
            }
            for future in tqdm(
                    as_completed(future_to_index),
                    desc=f"{model_name} api processing",
                    total=len(batch_messages)
            ):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    logger.error(f"An error occurred in collecting result {index=}: {e}")
        return results

class DefaultGenerationConfig:
    _gpt_thinking_model_series = ("gpt-o1", "gpt-o3", "gpt-o4")
    @classmethod
    def get_default_config(cls, model_name: str):
        if model_name.startswith(cls._gpt_thinking_model_series):
            return {
                "max_completion_tokens": 32768
            }
        else:
            return {
                'n': 1,
                'temperature': 0.5,
                'top_p': 0.75,
                'max_tokens': 8192,
                'timeout': 300
            }

class OpenaiAPICompletionService(BaseAPICompletionService):
    def __init__(self, api_endpoint, api_key, default_model_name):
        self.client = openai.OpenAI(
            api_key=api_key, 
            base_url=api_endpoint
        )
        super().__init__(api_endpoint, api_key, default_model_name)
    
    def fetch_supported_models(self):
        try:
            return [_.id for _ in self.client.models.list().data]
        except Exception as e:
            return []

    def __call__(self, messages: List[Dict], generation_config: dict, model_name: str, streaming: bool) -> Any:
        effective_generation_config = DefaultGenerationConfig.get_default_config(model_name)
        if generation_config is not None:
            effective_generation_config.update(generation_config)
        completion = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=streaming,
                extra_body={"return_reasoning": True}, #  if model_name.startswith("deepseek-r") else None
                **effective_generation_config
            )
        if streaming is True:
            is_in_thinking = False
            first_chunk = True
            for event in completion:
                if len(event.choices) > 0:
                    if first_chunk:
                        first_chunk = False
                        if hasattr(event.choices[0].delta, "reasoning_content"):
                            is_in_thinking = True
                            yield "<think>"
                        
                    if is_in_thinking:
                        if hasattr(event.choices[0].delta, "reasoning_content"):
                            if event.choices[0].delta.reasoning_content is not None:
                                yield event.choices[0].delta.reasoning_content
                            else:
                                continue
                        else:
                            is_in_thinking = False
                            yield "</think>"
                    
                    if not is_in_thinking:
                        if event.choices[0].delta.content is not None:
                            yield event.choices[0].delta.content
                    if event.choices[0].finish_reason == "stop":
                        yield None # means end
        else:
            logger.info(f"Total tokens: {completion.usage.total_tokens}, Completion tokens: {completion.usage.completion_tokens}")
            return [choice.message.content for choice in completion.choices]


class AzureOpenaiAPICompletionService(OpenaiAPICompletionService):
    def __init__(self, api_endpoint, api_key, api_version, default_model_name):
        self.client = openai.AzureOpenAI(
            api_key=api_key, 
            azure_endpoint=api_endpoint,
            api_version=api_version
        )
        BaseAPICompletionService.__init__(self, api_endpoint, api_key, default_model_name)
        self.api_version = api_version

service_type_map = {
    "openai": OpenaiAPICompletionService,
    "azure": AzureOpenaiAPICompletionService,
}


def load_services(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    services = {}
    for service_name, service_config in config['services'].items():
        service_type = service_config.pop('type')
        assert service_type in service_type_map
        services[service_name] = service_type_map[service_type](**service_config)
    
    for idx, (service_name, service_obj) in enumerate(services.items()):
        logger.info(f"[{idx+1}/{len(services)}] AI Service '{service_name}' ({service_obj.api_endpoint}, default={service_obj.default_model_name}) loaded with models: {service_obj.supported_models}")
    

    return services