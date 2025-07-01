import os
from src.ai_service import OpenaiAPICompletionService, AzureOpenaiAPICompletionService, load_services

# test_service = AzureOpenaiAPICompletionService(
#     api_endpoint=os.environ["AZURE_ENDPOINT"],
#     api_key=os.environ["AZURE_KEY"],
#     api_version=os.environ["AZURE_API_VERSION"],
#     default_model_name="gpt-4o"
# )

# test_service = OpenaiAPICompletionService(
#     api_endpoint=os.environ["CUSTOM_ENDPOINT"],
#     api_key=os.environ["CUSTOM_KEY"],
# )
# test_service.default_model_name = "gpt-3.5-turbo-1106"

all_test_services = load_services("tests/test_services.yaml")

test_service = all_test_services['azure']
print(test_service.supported_models)

print(test_service.generate("hello", generation_config={"n": 2}, streaming=False))

r = test_service.generate("hello", generation_config={"n": 1}, streaming=True)

for _ in r:
    if _ is None:
        print("<EOS>")
    else: 
        print(_, end="")

print(test_service.generate([
                {"role": "user", "content": "1+1=?"}
            ], streaming=True))

print(test_service.parallel_generate(
    [
        [{"role": "user", "content": "what is the capital of France?"}],
        [{"role": "user", "content": "AI is not "}],
    ]
))
