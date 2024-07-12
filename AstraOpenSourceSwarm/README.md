# Open Source Swarm
This directory shows how to use agency swarm with ANY open source or commercial models supported by [litellm](https://github.com/BerriAI/litellm) via [Astra Assistants](https://github.com/datastax/astra-assistants-api)

## Getting Started - Third Party API Providers

To get started with using agency swarm with models from third party (non-openai) api providers, follow these detailed steps:

1. **Install additional requirements**:
    From the OpenSourceSwarm directory, install the additional requirements using the `requirements.txt` file.
    ```bash
    poetry install
    ```
    If you don't have poettry installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer).
   
2. **Set Up your credentials**:
    Add the necessary API keys and configurations to your [.env file](https://github.com/datastax/astra-assistants-api/blob/main/client/.env.bkp) depending on which models you would like to use.
    ```bash
    cp .env.bkp .env
    ```
    and add your key(s).

    Note: you will also need an ASTRA_DB_APPLICATION_TOKEN which you can get [here](https://astra.datastax.com/), Astra Assistants persists assistant metadata in AstraDB (managed Apache Cassandra) and uses AstraDB for ANN, [here](https://www.datastax.com/pricing/astra-db) are the details on AstrDB pricing / free tier.

   
3. **Run Your Agent**:
    With the environment properly set up, you are now ready to activate your agency. Execute the following command within the AstraOpenSourceSwarm directory:
    ```bash
    poetry run python agency.py
    ```
    This command starts the gradio interface, which allows you to interact with your agents. Enjoy!


## Getting Started - Local Models with ollama


1. **Install additional requirements**:
   From the OpenSourceSwarm directory, install the additional requirements using the `requirements.txt` file.
    ```bash
    poetry install
    ```
   If you don't have poettry installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer).

2. **Run astra assistants and ollama locally with docker compose:**
   This is only required when running local ollama models:
    ```bash
    docker compose up -d
    ```
   If you don't have docker installed, you can install it by following the instructions [here](https://docs.docker.com/get-docker/).

   If using, ollama models, don't forget to first pull and run your model using the following command:
    ```bash
    curl http://localhost:11434/api/pull -d '{ "name": "llama3" }'
    ```

3. **Configure your .env**: 
   ```bash
   Add the necessary API keys and configurations to your [.env file](https://github.com/datastax/astra-assistants-api/blob/main/client/.env.bkp) depending on which models you would like to use.
    ```bash
    cp .env.bkp .env
    ```
   OLLAMA_API_BASE_URL should be set to http://ollama:11434 if you are using docker-compose. If you are using ollama on your localhost you can set it to http://localhost:11434
   if you are using any API provider models in combination with your ollama models remember to add your key(s) to the file.

   Note: you will also need an ASTRA_DB_APPLICATION_TOKEN which you can get [here](https://astra.datastax.com/), Astra Assistants persists assistant metadata in AstraDB (managed Apache Cassandra) and uses AstraDB for ANN, [here](https://www.datastax.com/pricing/astra-db) are the details on AstrDB pricing / free tier.


4. **Run Your Agent**:
   With the environment properly set up, you are now ready to activate your agency. Execute the following command within the AstraOpenSourceSwarm directory:
    ```bash
    poetry run python agency_ollama.py
    ```
   This command starts the gradio interface, which allows you to interact with your agents. Enjoy!



## Additional / Optional Steps

1. **Customize your agents**:
    You can customize your agents by changing the model they use, for example for the GroqAgent we set groq/llama3-8b-8192 as the model:
    ```python
    from agency_swarm.agents import Agent
    
    class GroqAgent(Agent):
        def __init__(self):
            super().__init__(
                model='groq/llama3-8b-8192', # Add your model here
            )
    ```
   Keep in mind, that **not all models support function calling** (custom tools). You can check support using litellm as described in the [litellm documentation](https://litellm.vercel.app/docs/completion/function_call#checking-if-a-model-supports-function-calling). For models that do not officialy support function calling, astra assistants will still attempt to get them to use tools via prompting which can be hit or miss.

   To create new agents, you can use the `create-agent-template` cli command:
   ```bash
   poetry run agency-swarm create-agent-template
   ```
