from instructor import OpenAISchema
from pydantic import Field
from typing import List, Literal

from agency_swarm import get_openai_client


class Dependency(OpenAISchema):
    type: Literal["class", "function", "import", "variable"] = Field(
        ..., description="The type of the dependency."
    )
    name: str = Field(
        ...,
        description="The name of the dependency, matching the import or definition.",
    )


class Dependencies(OpenAISchema):
    dependencies: List[Dependency] = Field(
        default_factory=list, description="The dependencies extracted from the file."
    )

    def append_dependencies(self, file: str, result: str) -> str:
        functions = [dep.name for dep in self.dependencies if dep.type == "function"]
        classes = [dep.name for dep in self.dependencies if dep.type == "class"]
        imports = [dep.name for dep in self.dependencies if dep.type == "import"]
        variables = [dep.name for dep in self.dependencies if dep.type == "variable"]
        result += f"File path: {file}\n"
        result += f"Functions: {functions}\nClasses: {classes}\nImports: {imports}\nVariables: {variables}\n\n"
        return result


def format_file_deps(v):
    client = get_openai_client()
    result = ""
    for file in v:
        # extract dependencies from the file using openai
        with open(file, "r") as f:
            content = f.read()

        resp = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class dependency resolver. You must extract the dependencies from the file provided.",
                },
                {
                    "role": "user",
                    "content": f"Extract the dependencies from the file '{file}'.\n\n{content}",
                },
            ],
            model="o1-mini",
            temperature=0,
            response_model=Dependencies,
        )

        result = resp.append_dependencies(file, result)

    return result
