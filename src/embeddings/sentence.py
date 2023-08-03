from sentence_transformers import SentenceTransformer
from typing import Optional

from ..utils.env import compose_model_id


def _load_model(model_name: str, organization: Optional[str]):
    model_id = compose_model_id(model_name, organization)
    print(model_id)
    model = SentenceTransformer(model_id)
    return model


def _encode(sentences, model):
    return model.encode(sentences)


HANDLERS = {
    "load": _load_model, "encode": _encode
}
