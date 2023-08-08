from sentence_transformers import SentenceTransformer
from typing import Any

from src.utils.env import compose_model_id
from ..base import Model


class EmbeddingModel(Model):
    model: Any

    
    def load(self):
        model_id = compose_model_id(self.id, prefix=self.org)
        print(f"Loading model {model_id}")
        self.model = SentenceTransformer(model_id)
        print(f"Model {model_id} loaded!")


    def encode(self, sentences):
        return self.model.encode(sentences)
