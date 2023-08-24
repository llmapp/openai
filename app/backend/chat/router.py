import json
import openai
import os
from dotenv import load_dotenv
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from .type import ChatCompletionRequest, ChatCompletionResponse


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/completions", response_model=ChatCompletionResponse)
async def stream_chat(request: ChatCompletionRequest):
    response = chat_completions(request)
    return EventSourceResponse(response, media_type="text/event-stream")


load_dotenv()
openai.api_base = os.getenv("OPENAI_API_BASE", None)
openai.api_key = os.getenv("OPENAI_API_KEY", "none")

FUNCTION_CALLING_LLMS = ["Qwen-7B-Chat"]

def chat_completions(request: ChatCompletionRequest):
    args = {
        "model": request.model,
        "messages": [_message_to_dict(m) for m in request.messages],
        "stream": request.stream,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
        "frequency_penalty": request.frequency_penalty,
        "presence_penalty": request.presence_penalty,
        "stop": request.stop
    }

    if request.model in FUNCTION_CALLING_LLMS:
        if request.functions:
            args["functions"] = [vars(f) for f in request.functions if f is not None]

        if request.function_call:
            args["function_call"] = vars(request.function_call) if type(request.function_call) is dict else request.function_call

    for chunk in openai.ChatCompletion.create(**args):
        yield "{}".format(json.dumps(chunk, ensure_ascii=True))
    yield '[DONE]'

def _filter_none(obj):
    return {k: v for k, v in obj.items() if v is not None}

def _message_to_dict(message):
    _dict = {}
    if message.role:
        _dict["role"] = message.role
    if message.content:
        _dict["content"] = message.content
    if message.function_call:
        _dict["function_call"] = vars(message.function_call)
    return _dict

