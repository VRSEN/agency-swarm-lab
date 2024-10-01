import litellm


def test_function_calling_support():
    models_with_support = [
        "gpt-4o-mini",
        "azure/gpt-4-1106-preview",
        "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "gemini/gemini-1.5-pro-latest",
        "claude-3-opus-20240229",
        "groq/mixtral-8x7b-32768",
    ]
    models_without_support = ["palm/chat-bison", "ollama/llama2"]

    for model in models_with_support:
        assert litellm.supports_function_calling(
            model
        ), f"Expected {model} to support function calling"

    for model in models_without_support:
        assert not litellm.supports_function_calling(
            model
        ), f"Expected {model} to not support function calling"


if __name__ == "__main__":
    test_function_calling_support()
    print("All tests passed successfully.")
