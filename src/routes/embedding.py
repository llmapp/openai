from fastapi import APIRouter

from ..type import EmbeddingsRequest

embedding_router = APIRouter()


@embedding_router.post("/embeddings")
@embedding_router.post("/engines/{model_name}/embeddings")
async def create_embeddings(request: EmbeddingsRequest, model_name: str = None):
    if request.model is None:
        request.model = model_name

    # TODO: Implement
    raise NotImplementedError()
