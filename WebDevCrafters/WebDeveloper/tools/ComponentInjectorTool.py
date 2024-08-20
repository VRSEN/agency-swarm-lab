import re
from types import UnionType
from pydantic import Field, model_validator
from typing import Dict, Any, List, Union
from .util.models import ReactComponent
from .ComponentCreatorTool import ComponentCreatorTool
import json, os, subprocess
from agency_swarm.tools import BaseTool

class ComponentInjectorTool(BaseTool):
    """
    Tool to inject a new component into an existing React component structure.
    Takes the file path of the component, additional import, the new component to inject, and the index of the target component.
    """
    file_path: str = Field(..., description="The file path of the existing React component.")
    additional_imports: List[str] = Field(..., description="Additional import statements for the new component. Example: ['import React from 'react']. Use empty list if no additional imports are needed.")
    component: Union[ReactComponent, str] = Field(..., description="The new component to inject.")
    target_component: str = Field(..., description="The name of the component into which the new component should be injected.")
    index: int = Field(..., description="The index of the target component to inject into (0-based index). In case when there are multiple components of the same type, use the index to specify which one to inject into.")
    insert_index: int = Field(..., description="The index at which to inject the new component. If the target component contains children, use the insert_index to specify which one to inject into. (0-based index)")

    class ToolConfig:
        strict = True
    
    def inject_component(self, parsed_json: Dict[str, Any], new_component: Dict[str, Any], target_type: str, index: int) -> Dict[str, Any]:
        """
        Inject a new component into the parsed JSON structure at the specified index within the target type.
        
        :param parsed_json: The parsed JSON structure of the JSX components.
        :param new_component: The new component to inject.
        :param target_type: The type of the component where the new component should be injected.
        :param index: The index (1-based) at which to inject the new component.
        :return: The modified JSON structure.
        """
        # Ensure parsed_json is a dictionary
        if not isinstance(parsed_json, dict):
            print(f"Error: Expected parsed_json to be a dict, but got {type(parsed_json)}")
            return parsed_json

        print("checking", parsed_json["type"], target_type, index)
        if parsed_json["type"] == target_type and index == 0:
            # Ensure 'children' key exists in props
            if "props" not in parsed_json:
                parsed_json["props"] = {}
            if "children" not in parsed_json["props"]:
                parsed_json["props"]["children"] = {}
            # Inject the new component at the specified insert index
            if isinstance(parsed_json["props"]["children"], dict):
                parsed_json["props"]["children"] = [parsed_json["props"]["children"]]
            elif not isinstance(parsed_json["props"]["children"], list):
                parsed_json["props"]["children"] = []
            parsed_json["props"]["children"].insert(self.insert_index, new_component)
            print('injected', parsed_json["props"]["children"])
        else:
            # Recursively search in children
            if "props" in parsed_json and "children" in parsed_json["props"]:
                children = parsed_json["props"]["children"]
                if isinstance(children, dict):
                    parsed_json["props"]["children"] = self.inject_component(children, new_component, target_type, index - (1 if parsed_json["type"] == target_type else 0))
                elif isinstance(children, list):
                    for i, child in enumerate(children):
                        # Ensure child is a dictionary before recursive call
                        if isinstance(child, dict):
                            parsed_json["props"]["children"][i] = self.inject_component(child, new_component, target_type, index - (1 if parsed_json["type"] == target_type else 0))
                        else:
                            print(f"Error: Expected child to be a dict, but got {type(child)}")
                else:
                    print(f"Error: Expected children to be a list or dict, but got {type(children)}")

        return parsed_json
    
    def parse_jsx_to_json(self, code, imports, logic):
        current_dir = os.getcwd()

        os.chdir(self._shared_state.get('app_directory', "./"))

        # Extract the return statement JSX code
        return_start = code.find("return (") + len("return (")
        return_end = code.find(");", return_start)
        return_jsx = code[return_start:return_end].strip()
        
        # Convert ES6 imports to CommonJS requires
        commonjs_imports = []
        for imp in imports:
            if imp.startswith('import'):
                parts = imp.split(' from ')
                module = parts[1].strip().strip(';').strip("'").strip('"')
                if '{' in parts[0]:
                    names = parts[0].split('{')[1].split('}')[0].strip()
                    commonjs_imports.append(f"const {{ {names} }} = require('{module}');")
                else:
                    name = parts[0].split(' ')[1]
                    commonjs_imports.append(f"const {name} = require('{module}');")
            else:
                commonjs_imports.append(imp)

        commonjs_imports.append(f"const {{serialize}} = require('react-serialize');")
        commonjs_imports = list(set(commonjs_imports))
        commonjs_imports = "\n".join(commonjs_imports)

        def nullify_logic(ts_code):
                # Convert React useState array destructuring to [null, null]
                ts_code = re.sub(r'const\s+\[(\w+),\s*(\w+)\]\s*=\s*useState\([^\)]*\);', r'const [\1, \2] = [null, null];', ts_code)

                # Convert all const functions (including arrow functions) to null
                ts_code = re.sub(r'const\s+(\w+)\s*=\s*\(.*?\)\s*=>\s*{[^}]*};', r'const \1 = null;', ts_code, flags=re.DOTALL)

                # Convert remaining const declarations to null
                ts_code = re.sub(r'const\s+(\w+)\s*=\s*.*?;', r'const \1 = null;', ts_code)
                
                # Convert all standard functions to null
                ts_code = re.sub(r'function\s+(\w+)\s*\(.*?\)\s*{[^}]*}', r'const \1 = null;', ts_code, flags=re.DOTALL)

                return ts_code
        
        logic = nullify_logic(logic)

        # Create a temporary JavaScript file to run the react-serialize package
        with open('parse_jsx.jsx', 'w') as js_file:
            js_content = f"""
                {commonjs_imports}
                {logic}
                const jsx = {return_jsx};
                const json = serialize(jsx);
                console.log(json);
            """
            js_file.write(js_content)

        # Transpile the JSX file using Babel
        subprocess.run(['npx', 'babel', 'parse_jsx.jsx', '--presets', '@babel/preset-react', '-o', 'transpiled.js'], check=True, shell=True)

        # Run the transpiled JavaScript file and capture the output
        result = subprocess.run(['node', 'transpiled.js'], capture_output=True, text=True)
        
        # Clean up the temporary files
        # os.remove('parse_jsx.jsx')
        os.remove('transpiled.js')

        if result.returncode != 0:
            raise Exception(f"Error executing Node.js script: {result.stderr}")

        print(result.stdout)

        os.chdir(current_dir)

        return json.loads(result.stdout)
    
    def extract_component_logic(self, code: str) -> str:
        """
        Extracts the logic (state and functions) from a React functional component.

        Parameters:
        code (str): The entire code of the React component.

        Returns:
        str: The extracted logic as a string, or an empty string if no match is found.
        """
        # Regex to capture everything inside the component before the return statement
        regex = r'const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{([\s\S]*?)(?=\s+return\s*[\(\<])'
        
        # Search for the pattern in the provided code
        match = re.search(regex, code)
        
        # Return the matched logic or an empty string if no match is found
        if match and match.group(1):
            return match.group(1).strip()
        else:
            return ""

    def render_json_to_jsx(self, component: Union[Dict[str, Any], str], indent: int = 0) -> str:
        """
        Convert the JSON structure of the component back into JSX.
        
        :param component: The JSON structure of the React component.
        :param indent: The current indentation level.
        :return: The JSX string.
        """
        if component is None:
            return ""

        if isinstance(component, str):
            return component
        
        indent_str = " " * indent
        props = component.get("props", {})
        children = props.pop("children", "")  # Remove children from props
        
        if component["type"] == "text":
            return f"{indent_str}{children}"
        
        props_str = " ".join([f'{key}={json.dumps(value)}' for key, value in props.items()])
        
        if children:
            if isinstance(children, list):
                children_str = "\n".join([self.render_json_to_jsx(child, indent + 2) for child in children])
            elif isinstance(children, dict):
                children_str = self.render_json_to_jsx(children, indent + 2)
            else:
                children_str = str(children)
            
            return f"{indent_str}<{component['type']} {props_str}>\n{children_str}\n{indent_str}</{component['type']}>"
        else:
            return f"{indent_str}<{component['type']} {props_str} />"
    
    def get_imports(self, code: str) -> List[str]:
        import_lines = []
        for line in code.split('\n'):
            if line.startswith('import'):
                import_lines.append(line)
        return import_lines

    def run(self):
        # Read the file
        with open(self.file_path, 'r') as file:
            code = file.read()

        logic = self.extract_component_logic(code)

        import_lines = self.get_imports(code)

        parsed_jsx_json = self.parse_jsx_to_json(code, import_lines + self.additional_imports, logic)

        # Print the type of parsed_jsx_json
        print(f"Type of parsed_jsx_json: {type(parsed_jsx_json)}")
        
        if isinstance(self.component, str):
            self.component = ReactComponent(type='text', children=self.component)

        modified_json = self.inject_component(parsed_jsx_json, self.component.custom_dump(), self.target_component, self.index)

        print(modified_json)
        
        # Render the modified structure back to JSX
        rerendered_jsx = self.render_json_to_jsx(modified_json)

        component_name = self.file_path.split('/')[-1].split('.')[0]

        # add indentation to rerendered_jsx
        rerendered_jsx = rerendered_jsx.replace('\n', '\n' + ' ' * 8)

        print(rerendered_jsx)

        print(os.getcwd())

        result = ComponentCreatorTool(
            file_path=self.file_path,
            name=component_name,
            logic=logic,
            imports=import_lines + self.additional_imports,
            return_component=ReactComponent(type='text', children=rerendered_jsx)
        ).run()

        # # Save the JSX to the file
        # with open(self.file_path, "w") as file:
        #     file.write(final_code)

        return result
    
    # @model_validator(mode='after')
    # def validate_shared_state(self):
    #     file_name = os.path.basename(self.file_path)
    #     if file_name not in self._shared_state.get('read_files'):
    #         raise ValueError("Please read this file first with the FileReader tool.")
    #     return self

    
if __name__ == "__main__":
    # tool = ComponentInjectorTool(
    #     file_path="./app.js",
    #     additional_imports=["import PropTypes from 'prop-types';"],
    #     target_component="button",
    #     index=0,
    #     insert_index=1,
    #     component=ReactComponent(type="button", props={}, children=[ReactComponent(type="span", props={}, children=[ReactComponent(type="text", children="Hello, world!")])])
    # )
    tool = ComponentInjectorTool(
        file_path="index.tsx",
        additional_imports=["import WelcomeSection from '../src/components/WelcomeSection';"],
        target_component="main",
        index=0,
        insert_index=0,
        component={"type":"WelcomeSection","props":{},"children":[]}
    )
    print(tool.run())