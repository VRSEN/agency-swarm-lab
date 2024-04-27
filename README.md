# Agency Swarm Lab
Welcome to the Agency Swarm Lab repository! This is a collaborative space where we showcase the incredible capabilities of custom AI agent teams developed using the [Agency Swarm](https://github.com/VRSEN/agency-swarm) framework.

## Getting Started 

### Local Installation

To get started with creating your own custom AI agency using the Agency Swarm Lab, follow these detailed steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/VRSEN/agency-swarm-lab.git
    ```

2. **Install Global Requirements**: Navigate to the root directory of the cloned repository and install the global requirements using the `requirements.txt` file. This will set up the necessary environment for running the Agency Swarm framework.

    ```bash
    cd agency-swarm-lab
    pip install -U -r requirements.txt
    ```

3. **Choose an Agency**: Decide which agency you would like to run or explore. Each agency is contained in its own folder within the repository.

4. **Install Agency-Specific Requirements**: Navigate into the directory of the agency you've chosen. Each agency may have its own `requirements.txt` file, which specifies additional dependencies necessary for that particular agency.

    ```bash
    cd path/to/your-chosen-agency
    pip install -r requirements.txt
    ```

5. **Set Up the `.env` File**: All agencies in the Agency Swarm Lab utilize OpenAI's API for their operations. To enable this functionality, you must provide your OpenAI API key.

    - Create a `.env` file in the chosen agency's folder.
    - Add your OpenAI API key to this file as follows:

        ```
        OPENAI_API_KEY='your_openai_api_key_here'
        # ...add other environment variables here if needed
        ```

    Dropping this `.env` file into the agency folder allows the system to authenticate with OpenAI's services seamlessly.

6. **Run Your Agency**: With the environment properly set up, you are now ready to activate your agency. Execute the following command within the agency's directory:

    ```bash
    python agency.py
    ```

    This command starts the operation of your custom AI agency, demonstrating the collaborative power of AI agents in accomplishing complex tasks.

### Docker Installation (recommended)


Running agencies in docker is safer as it does not affect your local file system. You will need to ensure that you had docker installed. For installation instructions, please refer to the [official Docker documentation](https://docs.docker.com/get-docker/).

1. **Clone and navigate into the Repository**.

    ```bash
    git clone https://github.com/VRSEN/agency-swarm-lab.git
    cd agency-swarm-lab
    ```
   
2. **Build the Docker Image**.

    ```bash
   docker build -t vrsen/agency-swarm -f path/to/your/Dockerfile .
    ```
   
    The command breakdown is as follows:
      - `-t vrsen/agency-swarm` is the name you give to the Docker image that you are generating.
      - `-f path/to/your/Dockerfile` specifies the path to the Dockerfile that you will use to build the image. The Dockerfile is located in the root of the repository.
   
3. **Run the Docker Image**: Use this command from the root of the repository. Make sure to replace `<YourOpenAIKey>` with your actual OpenAI API key.

    ```bash
    docker run -it -v ./:/app --rm -p 7860:7860 -e OPENAI_API_KEY=<YourOpenAIKey> vrsen/agency-swarm
    ```
   The command breakdown is as follows:

   - `-it` is used to start an interactive session with the Docker container.
   - `--rm` is used to delete the container after you have finished using it (any files in your mapped folder will be safe).
   - `-p 7860:7860` port forwards port 7860 for Gradio, should you wish to run Gradio from inside the Docker container after generating the code.
   - `-v ./:/app` maps the current directory with all the agencies to `/app` inside the Docker container.
   - `-e OPENAI_API_KEY=<YourOpenAIKey>` is where you put your OpenAI API key.
   - `vrsen/agency-swarm` the name you gave to the Docker image that you generated. 
   

4. **Install Agency-Specific Requirements** (inside Docker Image): Navigate into the directory of the agency you've chosen inside your docker image and install the requirements.

    ```bash
    cd path/to/your-chosen-agency
    pip install -r requirements.txt
    ```
   
5. **Run agency.py** (inside Docker Image): With the environment properly set up, you are now ready to activate your agency. Execute the following command within the agency's directory:

    ```bash
    python agency.py
    ```

# Contributing
We encourage contributions to the Agency Swarm Lab! If you have developed a custom AI agency using the Agency Swarm framework and would like to share it, please submit a pull request with your project.

# Stay Updated
Don't forget to subscribe to our [YouTube channel](https://youtube.com/@vrsen?si=l_6znuALa3IOl6ft) for tutorials and updates on the Agency Swarm framework and the amazing projects being developed with it.

Thank you for exploring the Agency Swarm Lab. Together, let's transform the future of work with AI.
