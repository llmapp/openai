from pydantic import BaseModel
from typing import Any, List

from .stable_diffusion import HANDLERS as STABLE_DIFFUSION_HANDLERS
from ..utils.logger import get_logger

logger = get_logger(__name__)

handler_map = {
    "stable-diffusion-xl-base-0.9": STABLE_DIFFUSION_HANDLERS,
    "stable-diffusion-xl-base-1.0": STABLE_DIFFUSION_HANDLERS,
}


class DiffuseModel(BaseModel):
    id: str
    pipe: Any


models: List[DiffuseModel] = []


def get_model(model_id: str = "stable-diffusion-xl-base-0.9"):
    global models

    if handler_map.get(model_id) is None:
        raise ValueError(f"Model {model_id} not found")

    model = next((m for m in models if m.id == model_id), None)

    if model is None:
        handlers = handler_map.get(model_id)
        logger.info(f"Loading model {model_id} ...")
        pipe = handlers.get("load")(model_id)
        logger.info(f"Model {model_id} loaded!")
        model = DiffuseModel(id=model_id, pipe=pipe)
        models.append(model)

    return model
