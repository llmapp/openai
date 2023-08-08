from fastapi import APIRouter

from ..models import list
from ..type import ModelList, ChatMessage

models_router = APIRouter(prefix="/models")


@models_router.get("", response_model=ModelList)
async def list_models():
    return ModelList(data=list())

@models_router.get("/test")
async def test():
    model_id = "Qwen-7B-Chat"
    from ..models import get_model
    model = get_model(model_id)

    response = model.chat(messages=[ChatMessage(role="user", content="你好")])

    return {"test": response}