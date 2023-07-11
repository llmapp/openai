from fastapi import APIRouter

from ..type import ModelCard, ModelList

models_router = APIRouter(prefix="/models")


@models_router.get("", response_model=ModelList)
async def list_models():
    global model_args
    model_card = ModelCard(id="gpt-3.5-turbo")
    return ModelList(data=[model_card])
