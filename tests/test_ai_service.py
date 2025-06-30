import os
from src.ai_service import AzureOpenaiAPICompletionService

test_service = AzureOpenaiAPICompletionService(
    api_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ["AZURE_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
    model_name="gpt-4o"
)

print(test_service.generate("hello", generation_config={"n": 2}))

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
