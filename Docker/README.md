# Docker

Some initial work to develop a Docker version of Agency Swarm. The intention behind this is to allow people to use Agency Swarm without potential issues with their local development environment.

## Building the Docker image

You can build the docker image by cloning this repository and running the docker build command. You will need to ensure that you had docker installed.

```bash
git clone https://github.com/VRSEN/agency-swarm-lab.git
cd agency-swarm-lab/Docker
docker build -t VRSEN/agency-swarm .
```

## Running the Docker image

Launch the container in interactive mode, map /app to your desired directory, and provide your OpenAI key:

```bash
docker run -it --rm -v <YourLocalDirectory>:/app -p 7860:7860 -e OPENAI_API_KEY=<YourOpenAIKey> VRSEN/agency-swarm

# For example 
# docker run -it --rm -v ./work_dir:/app -p 7860:7860 -e OPENAI_API_KEY=<YourOpenAIKey> VRSEN/agency-swarm
```

Make sure to replace with your directory path and <OPENAI_API_KEY> with your actual OpenAI API key.

- `-it` is used to start an interactive session with the Docker container.
- `--rm` is used to delete the container after you have finished using it (any generated files in your mapped volume will be safe).
- `-v <YourLocalDirectory>:/app` maps a directory of your choosing to `/app` inside the Docker container. This is where your generated code will go.
- `-p 7860:7860` port forwards port 7860 for Gradio, should you wish to run Gradio from inside the Docker container after generating the code.
- `-e OPENAI_API_KEY=<YourOpenAIKey>` is where you put your OpenAI API key.
- `VRSEN/agency-swarm` the name you gave to the Docker image that you generated in [Building the Docker image](#building-the-docker-image).
