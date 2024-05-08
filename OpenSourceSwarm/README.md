# Open Source Swarm
This directory shows how to use agency swarm with ANY open source or commercial models supported by [litellm](https://github.com/BerriAI/litellm).

## Getting Started

To get started with using my framework with open source models, follow these detailed steps:

1. **Install additional requirements**:
   From the OpenSourceSwarm directory, install the additional requirements using the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Set Up `litellm_config.yaml`**:
   Add the necessary API keys and configurations to the `litellm_config.yaml` file, depending on which models you would like to use. For example, for anthropic models, you would add the following configuration:
    ```yaml
     - model_name: anthropic/claude-3-opus-20240229
       litellm_params:
         model: anthropic/claude-3-opus-20240229
         api_key: <YOUR_ANTRHOPIC_API_KEY>
    ```
    If using, ollama models, don't forget to first pull and run your model using the following command:
    ```bash
   ollama pull llama3
    ```

3. **Run litellm proxy server**:
   To use the open-assistant-api, you will need to run the litellm proxy server using your configuration fileL
   ```bash
   litellm --config litellm_config.yaml
   ```
4. **Customize your agents**:
   You can now customize your agents by adding your own models and configurations to the `litellm_config.yaml` file. For example, to use olama models, you would add the following configuration:
    ```python
    from agency_swarm.agents import Agent
    
    class LlamaAgent(Agent):
        def __init__(self):
            super().__init__(
                model='ollama/llama3', # Add your model here
            )
    ```
   Keep in mind, that **not all models support function calling** (custom tools). You can check support using litellm as described in the [litellm documentation](https://litellm.vercel.app/docs/completion/function_call#checking-if-a-model-supports-function-calling).

   To create new agents, you can use the `create-agent-template` cli command:
    ```bash
    agency-swarm create-agent-template
    ```

5. **Pull open-assistant-api repo:**
   Pull the open-assistant-api repo using the following command:
   ```bash
   git clone https://github.com/VRSEN/open-assistant-api.git
   ```
   Currently, you have to pull it from my fork, as the original repo contains a bug with submitting tool outputs. You can find the original repo [here](https://github.com/MLT-OSS/open-assistant-api).

6. **Adjust the docker-compose file:**
   Adjust the `docker-compose.yml` file in the open-assistant-api directory to use the litellm proxy server:
   ```yaml
      OPENAI_API_BASE: http://host.docker.internal:4000/v1
      OPENAI_API_KEY: xxx
   ```
   This configuration connects to your litellm proxy server, which is running on port 4000. You can find more information on how to set up the litellm proxy server [here](https://litellm.vercel.app/docs/proxy/quick_start).

7. **Run the API:**
    Navigate to the open-assistant-api directory and run the API using the following command:
    ```bash
    docker compose up -d
    ```
   If you don't have docker installed, you can install it by following the instructions [here](https://docs.docker.com/get-docker/).

8. **Replace OpenAI Client**:
    Replace the OpenAI client with the OpenAssistant client in the `agency.py` file:
    ```python
    client = OpenAI(
        base_url="http://127.0.0.1:8086/api/v1", # Base url of the open-assistant-api
        api_key="xxx", # Not needed for open-assistant-api
        max_retries=5,
        default_headers={
            "OpenAI-Beta": "assistants=v1"
        }
    )
    set_openai_client(client)
    ```
9. **Add imports and initilize your agency**:
    Add all your agent imports to the `agency.py` file and initialize them. For example:
    ```python
    from agency_swarm.agents import CEO
    from agency_swarm.agents import LlamaAgent
    from agency_swarm.agency import Agency
    from .demo_gradio import demo_gradio
   
    ceo = CEO()
   
    llama_agent = LlamaAgent()
    
    agency = Agency([ceo, [ceo, llama_agent]])
   
   if __name__ == '__main__':
       demo_gradio(agency)
    ```
   Note, that you will have to use a slightly modified version of the `demo_gradio` function, provided in `demo_gradio.py` file, as the OpenAssistant API is not fully stable with streaming yet.  

    Also, if your model does not support function calling, **this agent will not be able to communicate with other agents. So, it must be included as the last agent in the list.**
   
10. **Run Your Agent**:
    With the environment properly set up, you are now ready to activate your agency. Execute the following command within the OpenSourceSwarm directory:
    ```bash
    python agency.py
    ```
    This command starts the gradio interface, which allows you to interact with your agents. Enjoy!