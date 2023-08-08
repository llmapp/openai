from typing import Optional

from ..type import ModelCard

class Model:
    id: str
    name: str
    org: str
    owner: str

    def __init__(self, model: str, name: Optional[str]=None, owner: Optional[str]=None):
        segs = model.split("/")
        if len(segs) != 2 or segs[0].strip() == "" or segs[1].strip() == "":
            raise ValueError(f"Invalid model name {model}")

        org, id = segs

        self.id = id
        self.org = org
        self.name = name if name is not None else id
        self.owner = owner if owner is not None else org

    def load(self):
        return self

    
    def to_card(self):
        return ModelCard(id=self.id, name=self.name, owned_by=self.owner)
    
    def __str__(self):
        return f"{self.org}/{self.id}"

