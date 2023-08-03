import tiktoken
from fastapi import APIRouter

from ..embeddings import models, get_model
from ..type import EmbeddingsRequest, EmbeddingsResponse, UsageInfo

embedding_router = APIRouter()


@embedding_router.post("/embeddings")
@embedding_router.post("/engines/{model_name}/embeddings")
async def create_embeddings(request: EmbeddingsRequest, model_name: str = None):
    if request.model is None:
        request.model = model_name

    embedding_model = get_model(request.model)
    encode = models.get(request.model).get("encode")

    inputs = _process_inputs(request)

    data, token_num = [], 0
    batches = [inputs[i: min(i + 1024, len(inputs))] for i in range(0, len(inputs), 1024)]

    for num_batch, batch in enumerate(batches):
        payload = {"embedding_model": embedding_model, "encode": encode, "input": batch}
        embedding = _get_embedding(payload)
        data += [
            {"object": "embedding", "embedding": emb, "index": num_batch * 1024 + i} for i, emb in enumerate(embedding["embedding"])
        ]
        token_num += embedding["token_num"]

    return EmbeddingsResponse(
        data=data,
        model=request.model,
        usage=UsageInfo(
            prompt_tokens=token_num,
            total_tokens=token_num,
            completion_tokens=None,
        ),
    ).model_dump(exclude_none=True)


def _process_inputs(request: EmbeddingsRequest):
    inputs = request.input
    if isinstance(inputs, str):
        inputs = [inputs]
    elif isinstance(inputs, list):
        if isinstance(inputs[0], int):
            decoding = tiktoken.model.encoding_for_model(request.model)
            inputs = [decoding.decode(inputs)]
        elif isinstance(inputs[0], list):
            decoding = tiktoken.model.encoding_for_model(request.model)
            inputs = [decoding.decode(text) for text in inputs]

    return inputs


def _get_embedding(payload):
    input, embedding_model, encode = payload["input"], payload["embedding_model"], payload["encode"]
    embeddings = encode(input, embedding_model.model)

    return {
        "embedding": embeddings.tolist(),
        "token_num": sum([len(i) for i in payload["input"]])
    }
