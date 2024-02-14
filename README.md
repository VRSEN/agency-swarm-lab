# Agency Swarm Lab
Welcome to the Agency Swarm Lab repository! This is a collaborative space where we showcase the incredible capabilities of custom AI agent teams developed using the [Agency Swarm](https://github.com/VRSEN/agency-swarm) framework.

## Getting Started

To get started with creating your own custom AI agency using the Agency Swarm Lab, follow these detailed steps:

1. **Clone the Repository**: First, clone the Agency Swarm Lab repository to your local machine to access the framework and the example agencies.

    ```bash
    git clone https://github.com/VRSEN/agency-swarm-lab.git
    ```

2. **Install Global Requirements**: Navigate to the root directory of the cloned repository and install the global requirements using the `requirements.txt` file. This will set up the necessary environment for running the Agency Swarm framework.

    ```bash
    cd agency-swarm-lab
    pip install -r requirements.txt
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
        ```

    Dropping this `.env` file into the agency folder allows the system to authenticate with OpenAI's services seamlessly.

6. **Run Your Agency**: With the environment properly set up, you are now ready to activate your agency. Execute the following command within the agency's directory:

    ```bash
    python agency.py
    ```

    This command starts the operation of your custom AI agency, demonstrating the collaborative power of AI agents in accomplishing complex tasks.

# Contributing
We encourage contributions to the Agency Swarm Lab! If you have developed a custom AI agency using the Agency Swarm framework and would like to share it, please submit a pull request with your project.

# Stay Updated
Don't forget to subscribe to our [YouTube channel](https://youtube.com/@vrsen?si=l_6znuALa3IOl6ft) for tutorials and updates on the Agency Swarm framework and the amazing projects being developed with it.

Thank you for exploring the Agency Swarm Lab. Together, let's transform the future of work with AI.
