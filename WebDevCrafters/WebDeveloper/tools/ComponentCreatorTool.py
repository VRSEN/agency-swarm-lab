from agency_swarm.tools import BaseTool
from pydantic import Field, BaseModel, ConfigDict
from typing import List, Dict, Any, Union
import json, os
from .util.models import ReactComponent

class ComponentCreatorTool(BaseTool):
    """
    Tool to generate a functional React component from a JSON structure.
    Takes imports, a list of React components each with a type, logic, props, and children.
    Generates the final React component code and saves it into a file.

    The final component has the following structure:
    ```
    const {self.name} = () => {{
    {self.logic}

        return (
    {self.return_component.render(indent=4)}
        );
    }};

    export default {self.name};
    ```
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., description="The name of the main React component. Examples: App, Button, Header, Footer")
    file_path: str = Field(..., description="The path to the file to save the React component code. Example: /Users/johndoe/projects/my-app/components/Button.tsx")
    imports: List[str] = Field(..., description="List of imports for the React component. Examples: 'import React from 'react';', 'import PropTypes from 'prop-types';'")
    logic: str = Field(..., description="The logic of the component. For example, submitting a form or handling a click event. Leave empty string if no logic is needed. Example: const handleClick = () => console.log('Hello, world!');\n\nconst handleSubmit = (event) => {\n  event.preventDefault();\n  console.log('Form submitted');\n}")
    return_component: Union[ReactComponent, str] = Field(..., description="""The return value of the component. For example, a button or a form.
                                                         Example input: {"type":"div","props":{},"children":[{"type":"text","props":{},"children":"This is a test component."},{"type":"text","props":{},"children":"This component is created to test the ComponentCreatorTool functionality."}]}""")

    class ToolConfig:
        strict = True
    
    def run(self):
        """
        Generate the React component code and save it into a file.
        """
        # Generate the imports
        imports_code = "\n".join(self.imports)

        # Generate the components code (assuming there's a single main component)
        components_code = self.return_component.render(indent=8) if isinstance(self.return_component, ReactComponent) else self.return_component

        # Combine everything into the final React component code
        final_code = f"""{imports_code}

const {self.name} = () => {{
{self.logic or ""}

    return (
{components_code}
    );
}};

export default {self.name};
"""
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Save the final code into a file, overwriting if it already exists
        with open(self.file_path, "w") as file:
            file.write(final_code)

        self._shared_state.set('files_read', self._shared_state.get('files_read', []) + [os.path.basename(self.file_path)])
        
        return f"React component code generated and saved to {self.file_path}. Full code:\n\n```{final_code}```"
    
if __name__ == "__main__":
    tool = ComponentCreatorTool(
        name="Header",
        file_path="src/components/Header.tsx",
        imports=["import React from 'react';", "import { AppBar, Toolbar, Typography, Button } from '@mui/material';"],
        logic="",
        return_component="""{"type":"div","props":{},"children":[{"type":"text","props":{},"children":"This is a test component."},{"type":"text","props":{},"children":"This component is created to test the ComponentCreatorTool functionality."}]}"""
    )
    print(tool.run())

    import json
    print(json.dumps(ComponentCreatorTool.openai_schema, indent=2))