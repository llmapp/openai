
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from typing import List

from ..llms import models, get_model
from ..llms.chatglm import chat as chat_chatglm, stream_chat as stream_chat_chatglm
from ..llms.baichuan import chat as chat_baichuan
from ..type import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, ChatMessage


chat_router = APIRouter(prefix="/chat")

COMPLETION_CHUNK = "chat.completion.chunk"


@chat_router.post("/completions", response_model=ChatCompletionResponse)
async def completions(request: ChatCompletionRequest):
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")

    if request.stream:
        return stream_chat(model_id=request.model, messages=request.messages)
    else:
        return chat(model_id=request.model, messages=request.messages)


def chat(model_id: str, messages: List[ChatMessage]):
    model_type = models.get(model_id)
    if model_type is None:
        raise ValueError(f"Model {model_id} not found")

    model, tokenizer = get_model(model_id)

    do_chat = None
    if model_type == "chatglm":
        do_chat = chat_chatglm
    if model_type == "baichuan":
        do_chat = chat_baichuan

    response, _ = do_chat(model, tokenizer, messages)

    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=response),
        finish_reason="stop"
    )
    return ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion")


def stream_chat(model_id: str, messages: List[ChatMessage]):
    model_type = models.get(model_id)
    if model_type is None:
        raise ValueError(f"Model {model_id} not found")

    model, tokenizer = get_model(model_id)

    do_stream_chat = None
    if model_type == "chatglm":
        do_stream_chat = stream_chat_chatglm

    generate = do_stream_chat(model, tokenizer, messages, model_id)
    return EventSourceResponse(generate, media_type="text/event-stream")
