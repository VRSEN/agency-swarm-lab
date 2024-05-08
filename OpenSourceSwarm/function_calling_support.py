import litellm

assert litellm.supports_function_calling(model="gpt-3.5-turbo") == True
assert litellm.supports_function_calling(model="azure/gpt-4-1106-preview") == True
assert litellm.supports_function_calling(model="palm/chat-bison") == False
assert litellm.supports_function_calling(model="ollama/llama2") == False
assert litellm.supports_function_calling(model="together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1") == True
assert litellm.supports_function_calling(model="gemini/gemini-1.5-pro-latest") == True
assert litellm.supports_function_calling(model="claude-3-opus-20240229") == True
assert litellm.supports_function_calling(model="groq/mixtral-8x7b-32768") == True