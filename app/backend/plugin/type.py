import json
from pydantic import BaseModel
from typing import Any, Optional, List


class Argument(BaseModel):
    name: str
    type: str
    required: Optional[bool] = False
    description: str


class Plugin(BaseModel):
    name: str
    description: str
    arguments: Optional[List[Argument]]

    name_for_human: Optional[str]
    description_for_human: Optional[str]

    def to_function(self):
        properties = {}
        for argument in self.arguments:
            properties[argument.name] = {"type": argument.type, "description": argument.description}

        func = {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "required": [arg.name for arg in self.arguments if arg.required],
                "properties": properties,
            }
        }

        return func

    def run(self, args: str) -> Any:
        try:
            params = json.loads(args)
        except Exception as _:
            return None

        return params
