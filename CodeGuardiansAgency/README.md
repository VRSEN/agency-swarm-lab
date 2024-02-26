# CodeGuardians Agency

Welcome to the **CodeGuardians Agency**, a custom GitHub code analysis agency created using the open-source agent orchestration framework, **Agency Swarm**. Our mission is to enforce Standard Operating Procedures (SOPs) for code quality across your projects, providing analysis comments directly on your pull requests to ensure maintainability, encapsulation, and overall code quality.

## Agency Structure

The **CodeGuardians Agency** is structured around three core agents:

- **CEO**: Initiates the analysis process and oversees the operation.
- **Code Analyzer**: Analyzes the code against predefined SOPs and identifies code quality issues.
- **Report Generator**: Generates reports on pull requests, highlighting any problematic lines of code according to the analysis.

## Tools

The CodeGuardians Agency utilizes several custom tools designed to streamline the code analysis process:

- **GitHub Pull Request Fetcher**: Utilizes the GitHub API to fetch all changes from a pull request, saving time on manual review and API documentation research.

- **Code Analysis Tools**: Tailored specifically to your SOPs, these tools analyze the codebase for adherence to quality standards, identifying issues like direct database access or improper encapsulation.

## Usage

The CodeGuardians Agency is designed to run automatically as part of your GitHub Actions workflow. It triggers on pull request events, analyzing the codebase and providing feedback directly within the pull request comments.

### Adjusting Tools and Instructions

You may need to adjust the provided tools and instructions to fit your specific code quality standards and SOPs. This customization process involves:

1. Defining your code quality standards within the Code Analyzer agent instructions.
2. Tailoring the GitHub Pull Request Fetcher to filter for relevant file types and changes.
3. Customizing the Report Generator to format and deliver actionable feedback within pull requests.

## Deployment

To deploy the **CodeGuardians Agency** in production:

1. Copy the adjusted agency folder into your project repository.
2. Add your OpenAI API key and GitHub token to an environment file for secure access.
3. Create a GitHub workflow that triggers the agency to run on every pull request, ensuring continuous code quality checks.

## Possible Improvements

### Enhanced Code Fixing Capabilities

Future versions could include agents capable of not just identifying but also fixing problematic code snippets, pushing the corrected code to GitHub automatically.

### Detailed Line-by-Line Comments

Improving the agency to leave comments on specific lines of code where issues are detected could enhance clarity and speed up the review process.

### Expansion to Additional Programming Languages

While the current focus might be on TypeScript files, expanding the agency's capabilities to cover more programming languages could broaden its applicability.

## Conclusion

The **CodeGuardians Agency** exemplifies how AI can transform code review and quality assurance processes, aligning with SOPs and enhancing team collaboration. By automating code analysis and reporting, teams can maintain high code quality standards efficiently.