from pydantic import BaseModel
from typing import Any, List


from .sentence import HANDLERS as SENTENCE_HANDLERS
from ..utils.logger import get_logger

logger = get_logger(__name__)

models = {
    "gte-large": SENTENCE_HANDLERS,
    "e5-large-v2": SENTENCE_HANDLERS,
    #     "multilingual-e5-large": SENTENCE_HANDLERS
}

organizations = {
    "gte-large": "thenlper",
    "e5-large-v2": "intfloat",
    "multilingual-e5-large": "intfloat"
}


class EmbeddingModel(BaseModel):
    id: str
    model: Any = None


_models: List[EmbeddingModel] = []


def get_model(model_id: str = "gte-large"):
    global _models

    if models.get(model_id) is None:
        raise ValueError(f"Model {model_id} not found")

    _model = next((m for m in _models if m.id == model_id), None)

    if _model is None:
        handlers = models.get(model_id)
        logger.info(f"Loading model {model_id} ...")
        model = handlers.get("load")(model_id, organizations[model_id])
        logger.info(f"Model {model_id} loaded!")

        _model = EmbeddingModel(id=model_id, model=model)
        _models.append(_model)

    return _model
