from uuid import uuid4, UUID
from fastapi import APIRouter

chat_router = APIRouter(prefix="/chat")


@chat_router.get("/completions")
async def completions():
    return {'message': 'completions'}
