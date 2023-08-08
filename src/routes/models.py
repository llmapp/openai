from fastapi import APIRouter, HTTPException

from ..models import list, get_model
from ..type import ModelList, ModelCard

models_router = APIRouter(prefix="/models")


@models_router.get("", response_model=ModelList)
async def list_models():
    return ModelList(data=list())

@models_router.get("/{id}", response_model=ModelCard)
async def retrieve_model(id: str):
    model = get_model(id, skip_load=True)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model {id} not found")
    return model.to_card()