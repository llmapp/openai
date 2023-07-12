from fastapi import APIRouter

from ..type import ModelCard, ModelList
from ..llms import get_models

models_router = APIRouter(prefix="/models")


@models_router.get("", response_model=ModelList)
async def list_models():
    model_list = get_models()
    model_cards = [ModelCard(id=id) for id in model_list]

    return ModelList(data=model_cards)
