from pydantic import BaseModel
from typing import Any, List

from .whisper import HANDLERS as WHISPER_HANDLERS
from ..utils.logger import get_logger

logger = get_logger(__name__)

models = {
    "whisper-large-v1": WHISPER_HANDLERS,
    "whisper-large-v2": WHISPER_HANDLERS,
    "whisper-medium": WHISPER_HANDLERS,
    "whisper-medium.en": WHISPER_HANDLERS,
    "whisper-small": WHISPER_HANDLERS,
    "whisper-small.en": WHISPER_HANDLERS,
    "whisper-base": WHISPER_HANDLERS,
    "whisper-base.en": WHISPER_HANDLERS,
    "whisper-tiny": WHISPER_HANDLERS,
    "whisper-tiny.en": WHISPER_HANDLERS,
}


class AudioModel(BaseModel):
    id: str
    model: Any


_models: List[AudioModel] = []


def get_model(model_id: str = "whisper-large-v2"):
    global _models

    if model_id == "whisper-1":
        model_id = "whisper-large-v2"

    if models.get(model_id) is None:
        raise ValueError(f"Model {model_id} not found")

    _model = next((m for m in _models if m.id == model_id), None)

    if _model is None:
        handlers = models.get(model_id)
        logger.info(f"Loading model {model_id} ...")
        model = handlers.get("load")(model_id)
        logger.info(f"Model {model_id} loaded!")

        _model = AudioModel(id=model_id, model=model)
        _models.append(_model)

    return _model
