
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from typing import List

from ..llms import models, get_model
from ..type import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice, ChatMessage, DeltaMessage


chat_router = APIRouter(prefix="/chat")


@chat_router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")

    if request.stream:
        return stream_chat(model_id=request.model, messages=request.messages)
    else:
        return chat(model_id=request.model, messages=request.messages)


def chat(model_id: str, messages: List[ChatMessage]):
    handlers = models.get(model_id)
    if handlers is None:
        raise ValueError(f"Model {model_id} not found")

    model, tokenizer = get_model(model_id)

    response, _ = handlers.get("chat")(model, tokenizer, messages)

    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=response),
        finish_reason="stop"
    )
    return ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion")


def stream_chat(model_id: str, messages: List[ChatMessage]):
    handlers = models.get(model_id)
    if handlers is None:
        raise ValueError(f"Model {model_id} not found")

    model, tokenizer = get_model(model_id)

    generate, stream_type = handlers.get("stream_chat")(model, tokenizer, messages)
    predict = _predict(model_id, generate, stream_type)
    return EventSourceResponse(predict, media_type="text/event-stream")


def _predict(model_id: str, generate, stream_type: str):
    yield _compose_chunk(model_id, DeltaMessage(role="assistant"))

    current_length = 0
    for response in generate:
        if stream_type == "delta":
            delta = response
        else:
            if stream_type == "tuple":
                new_response, _ = response
            elif stream_type == "string":
                new_response = response

            if len(new_response) == current_length:
                continue

            delta = new_response[current_length:]

            current_length = len(new_response)

        yield _compose_chunk(model_id, DeltaMessage(content=delta))

    yield _compose_chunk(model_id, DeltaMessage())
    yield '[DONE]'


def _compose_chunk(model_id: str, message: DeltaMessage):
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=message,
        finish_reason="stop"
    )
    chunk = ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion.chunk")

    return "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))
