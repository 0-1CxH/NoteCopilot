from .ai_service import load_services
from dataclasses import dataclass
import yaml

import logging

logger = logging.getLogger("AICopilot")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@dataclass
class AICopilotFunction:
    name: str
    description: str
    icon: str
    template: str
    model: str = None

class AICopilot:
    def __init__(self, ai_service_config_path, ai_function_config_path) -> None:
        self.ai_services = load_services(ai_service_config_path)

        self.default_service_name = list(self.ai_services.keys())[0]
        self.default_service = self.ai_services[self.default_service_name]
        self.default_model_name = self.default_service.default_model_name
        logger.info(f"Default AI Service: {self.default_service_name}, Default Model: {self.default_model_name}")
        
        with open(ai_function_config_path, 'r', encoding='utf-8') as f:
            functions_yaml = yaml.safe_load(f)
        self.ai_functions = {
            func['name']: AICopilotFunction(**func) for func in functions_yaml.get('functions', [])
        }
        self.system_message = functions_yaml.get('system_message')
        logger.info(f"Current System Message is: {self.system_message}") 
        # map functions to service and model
        self.func_to_serv_model_map = {}
        for func_name in self.ai_functions:
            func_object = self.ai_functions[func_name]
            if func_object.model is None:
                self.func_to_serv_model_map[func_name] = (self.default_service_name, self.default_model_name)
            else:
                # find the model in all services, and default is priority, if cannot find,  raise error
                found = False
                # Priority: default service first
                for service_name in [self.default_service_name] + [s for s in self.ai_services if s != self.default_service_name]:
                    service = self.ai_services[service_name]
                    if service.is_model_supported(func_object.model):
                        self.func_to_serv_model_map[func_name] = (service_name, func_object.model)
                        found = True
                        break
                if not found:
                    raise ValueError(f"Model '{func_object.model}' for function '{func_name}' not found in any AI service.")
        
        for idx, func_name in enumerate(self.ai_functions):
            logger.info(
                f"[{idx+1}/{len(self.ai_functions)}]AI Function Loaded: {func_name} - {self.ai_functions[func_name].description}"
                f"-- (service, model) = {self.func_to_serv_model_map[func_name]}"
            )
        
    
    def get_funcs(self, return_json=True):
        # Return the list of AI functions as a list of dicts
        # If return_json is False, return the list of AICopilotFunction objects
        self_obj = self if isinstance(self, AICopilot) else None
        if self_obj is None:
            raise ValueError("get_funcs must be called as an instance method")
        if return_json:
            return [
                {
                    "name": func.name,
                    "description": func.description,
                    "icon": func.icon,
                    "template": func.template,
                    "model": func.model,
                }
                for func in self_obj.ai_functions.values()
            ]
        else:
            return list(self_obj.ai_functions.values())

    def __call__(self, request_data):
        selected_func_name = request_data.get('selected_func_name', None)
        serv_, model_ = self.get_func_serv_model(selected_func_name)

        type_ = request_data['type']
        if type_ == "completion":
            query_ = "Read and analyze the following content, then try to continue writing it:\n{{content}}\n\nNote: start answer immediately, DO NOT GENERATE OTHER THINGS."
        elif type_ == "ask":
            query_ = request_data.get("query")
        else:
            return "Invalid Request Type"
        
        content_ = request_data['content']
        if content_.strip() == "":
            return "No Content Provided"
        
        if "{{content}}" in query_:
            if query_.count("{{content}}") > 1:
                logger.warning(f"Content will be repalced more than once!")
            query_ = query_.replace("{{content}}", content_)
        else:
            query_ = content_ + "\n\n"  + query_
        
        messages_ = []
        if self.system_message:
            messages_.append(
                {"role": "system", "content": self.system_message}
            )
        messages_.append(
            {"role": "user", "content": query_}
        )
        logger.info(f"Generate with {serv_.api_endpoint}, {model_}. Messages: {messages_}")
        return serv_.generate(
            messages = messages_,
            streaming = True,
            model_name = model_,
            generation_config = {'n': 1, 'max_tokens': 256,} if type_ == "completion" else None
        )
    
    def get_default_serv_model(self):
        return (self.default_service, self.default_model_name)
        
    def get_func_serv_model(self, func_name):
        if func_name in self.func_to_serv_model_map:
            service_name, model_name = self.func_to_serv_model_map[func_name]
            return (self.ai_services[service_name], model_name)
        else:
            return self.get_default_serv_model()