
from fastapi import APIRouter
from ..type import CompletionRequest


completion_router = APIRouter(prefix="/completions")


@completion_router.post()
async def create_completion(request: CompletionRequest):
    # TODO: Implement
    raise NotImplementedError()
