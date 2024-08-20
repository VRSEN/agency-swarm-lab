from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, List, Union
import json

class ReactComponent(BaseModel):
    type: str = Field(..., description="The type of the component. For simple text, use 'text'. For empty components (e.g. <></>), use 'empty'. Examples: Button, Header, Footer, div, span, text, empty")
    props: Dict[str, Any] = Field(default_factory=dict, description="The props of the component.")
    children: Union[str,  List['ReactComponent']] = Field(..., description="The children of the component. String is only allowed for 'text' type.")

    def custom_dump(self):
        # Prepare the basic component structure
        component = {
            "type": self.type,
            "props": self.props.copy(),  # Create a copy to avoid modifying the original props
        }

        # Handle children serialization
        if isinstance(self.children, list):
            component["props"]["children"] = [
                child.custom_dump() if isinstance(child, ReactComponent) else child
                for child in self.children
            ]
        else:
            component["props"]["children"] = self.children

        return component

    @model_validator(mode='after')
    def validate_children(self):
        if isinstance(self.children, str) and self.type != 'text':
            raise ValueError("Children must be a string for 'text' type.")
        
        if isinstance(self.children, list) and self.type != 'text':
            for child in self.children:
                if not isinstance(child, ReactComponent):
                    raise ValueError("Children must be a list of ReactComponent objects for non-'text' types.")
            
        if self.type == 'text' and isinstance(self.children, list):
            raise ValueError("Children must be a string for 'text' type.")
        
        return self

    class Config:
        arbitrary_types_allowed = True

    def render(self, indent=4):
        if self.type == 'text':
            return ' ' * indent + self.children
        elif self.type == 'empty':
            self.type = ""
        
        props_str = " ".join([f'{key}={json.dumps(value)}' if key != 'children' else '' for key, value in self.props.items()])
        props_str = props_str.strip()

        indent_str = ' ' * indent
        
        if isinstance(self.children, str):
            children_str = self.children
            return f"{indent_str}<{self.type}{' ' + props_str if props_str else ''}>{children_str}</{self.type}>"
        else:
            children_str = "\n".join([child.render(indent + 2) for child in self.children])
            if children_str:
                return f"{indent_str}<{self.type}{' ' + props_str if props_str else ''}>\n{children_str}\n{indent_str}</{self.type}>"
            else:
                return f"{indent_str}<{self.type}{' ' + props_str if props_str else ''} />"

    def get_logic(self):
        # Return the component's logic, if any
        return self.logic