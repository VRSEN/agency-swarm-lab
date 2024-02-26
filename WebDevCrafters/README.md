# Web Dev Crafters Agency

Welcome to the **Web Dev Crafters** agency, a custom AI agency created using the open-source agent orchestration framework, **Agency Swarm**. Our mission is to develop responsive web applications using Next.js and Material UI, leveraging the power of AI to streamline the web development process.

## Agency Structure

The **Web Dev Crafters** agency is designed with a collaborative structure where the CEO communicates with the designer, who in turn communicates with the web developer and copywriter. This ensures a seamless workflow from design to development.

## Installation

To install the required dependencies for this agency, run the following command:

```bash
pip install -r requirements.txt
```

Make sure you have `agency_swarm` and `npm` installed as well. For details on how to install `npm`, refer to the official [npm documentation](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

## Agents

Agents are created with specific roles:

- **Designer Agent**: Responsible for the UI/UX design, utilizing tools like the browser analysis tool.
- **Web Developer Agent**: Handles the development of the web application, equipped with tools like the directory navigator, file reader, and writer.
- **Copywriter Agent**: Creates compelling content for the website.
For the **Web Dev Crafters** agency, several custom tools were created for each agent to facilitate their tasks in the web development process. Below is a description of the tools created for each agent, as mentioned in the script:

## Tools

### Designer Agent Tools

- **Browser Analysis Tool**: This tool uses GPT-4V to analyze web pages and provide insights on design elements, color schemes, and layout. It helps the designer agent to ensure that the current web page aligns with the provided design.

### Web Developer Agent Tools

- **Directory Navigator Tool**: Utilizes the OS `change dir` method to navigate through directories. This simple yet effective tool helps the web developer agent to move around the file system and locate files necessary for web development.
  
- **File Reader Tool**: Opens and reads the content of files, returning the content as a string. This tool is essential for the web developer agent to read existing code files and make necessary adjustments or additions.
  
- **File Writer Tool**: Takes a filepath and content as input, then opens and writes the content to the file, confirming the action by returning a success message. This tool is crucial for creating new files or updating existing ones with new content.
  
- **Command Executor Tool**: Originally designed to execute commands using subprocess, it was deemed potentially dangerous and was planned to be modified. The idea was to restrict it to run only predefined safe commands, such as `npx create-next-app` or `npm run build`, to ensure the security and integrity of the development process.

- **List Directory Tool** (Proposed for the Web Developer Agent): This tool would list the contents of a directory, providing a view of the current directory tree as a string. It's aimed at enhancing the web developer agent's ability to manage and overview the project's file structure.

These tools are designed to automate specific tasks within the agency, reducing manual effort and streamlining the web development process. Each tool is tailored to the needs of its respective agent, ensuring they can perform their duties effectively and efficiently.

## Usage

Run your agency using the following command:

```bash
python agency.py
```

This command initiates the workflow, where each agent performs its designated tasks, from design to content creation and web development. The process is iterative, with continuous improvements based on feedback.

## Possible Improvements

### 1. Enhanced Instructions for Agents

Improving the clarity and specificity of instructions given to agents can significantly enhance the output quality. This involves refining the task descriptions and objectives for each agent, ensuring they have a clear understanding of the goals and constraints of their assignments. Enhanced instructions will lead to more accurate and aligned deliverables, reducing the need for revisions.

### 2. Proper Website Theming

Implementing a more systematic approach to website theming will ensure consistent styling across web pages. This can be achieved by developing a comprehensive theming tool or framework within the agency that allows for easy selection and application of themes, including colors, fonts, and layout patterns. Such a tool could leverage existing design systems or create a custom one that fits the agency's most common project types.

### 3. Generating Images for the Website with DALL-E 3

Integrating DALL-E 3 into the agency's toolkit to generate custom images and graphics for websites could significantly enhance the visual appeal and uniqueness of web projects. This could be added as a tools in a new `ImageGeneratorAgent` or integrated into the existing Designer Agent's workflow.

### 4. QA Testing

Incorporating advanced testing and quality assurance tools into the agency's workflow is crucial for delivering bug-free, high-quality websites. This could include automated unit testing, integration testing, and visual regression testing tools, specifically tailored to work with the technologies and frameworks used by the agency, such as Next.js and Material UI. This could also be achieved with a new `QAManagerAgent` that oversees the testing process and ensures the quality of the final product.

## Conclusion

The **Web Dev Crafters** agency demonstrates the potential for AI to automate future tasks. While agent development currently involves extensive iteration, it underscores the vast possibilities yet to be explored. By leveraging this foundation, it's conceivable to establish a fully automated web development agency capable of producing high-quality websites with minimal human input. 
