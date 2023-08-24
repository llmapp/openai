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

def chat_completions(request: ChatCompletionRequest):
    args = {
        "model": request.model,
        "messages": [_filter_none(vars(m)) for m in request.messages],
        "stream": request.stream,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
        "frequency_penalty": request.frequency_penalty,
        "presence_penalty": request.presence_penalty,
        "stop": request.stop
    }

    for chunk in openai.ChatCompletion.create(**args):
        yield "{}".format(json.dumps(chunk, ensure_ascii=True))
    yield '[DONE]'

def _filter_none(obj):
    return {k: v for k, v in obj.items() if v is not None}
