
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from typing import List

from ..llms import models, get_model
from ..llms.baichuan import chat as chat_baichuan, stream_chat as stream_chat_baichuan
from ..llms.chatglm import chat as chat_chatglm, stream_chat as stream_chat_chatglm
from ..llms.internlm import chat as chat_internlm, stream_chat as stream_chat_internlm
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
    model_type = models.get(model_id)
    if model_type is None:
        raise ValueError(f"Model {model_id} not found")

    model, tokenizer = get_model(model_id)

    do_chat = None
    if model_type == "chatglm":
        do_chat = chat_chatglm
    if model_type == "baichuan":
        do_chat = chat_baichuan
    if model_type == "internlm":
        do_chat = chat_internlm

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
    elif model_type == "baichuan":
        do_stream_chat = stream_chat_baichuan
    elif model_type == "internlm":
        do_stream_chat = stream_chat_internlm

    generate = do_stream_chat(model, tokenizer, messages)
    predict = _predict(model_id, generate)
    return EventSourceResponse(predict, media_type="text/event-stream")


def _predict(model_id: str, generate):
    yield _compose_chunk(model_id, DeltaMessage(role="assistant"))

    current_length = 0
    for response in generate:
        response_type = type(response)
        if response_type is str:
            new_response = response
        elif response_type is tuple:
            new_response, _ = response
        else:
            break

        if len(new_response) == current_length:
            continue

        yield _compose_chunk(model_id, DeltaMessage(content=new_response[current_length:]))

        current_length = len(new_response)

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
