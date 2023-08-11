
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from typing import Optional

from ..models import get_model
from ..models.llm import LlmModel
from ..type import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice, ChatMessage, DeltaMessage, FunctionCallResponse, UsageInfo
from ..utils.request import raise_if_invalid_model
from ..utils.function_call import need_function_call, build_chat_message, build_function_call_message, build_fc_args_message, build_fc_name_message


chat_router = APIRouter(prefix="/chat")


@chat_router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    model = get_model(request.model)
    raise_if_invalid_model(model, LlmModel)
    
    with_function_call = need_function_call(messages=request.messages, functions=request.functions)
    if with_function_call and model.org != "Qwen":
        raise HTTPException(status_code=400, detail="Invalid request format: functions only supported by Qwen-7B-Chat")

    kwargs = _gen_kwargs(request, model.tokenizer)
    if with_function_call:
        last = build_function_call_message(request.messages, request.functions)
        query = last.content
        request.messages[-1].content = query
        stop_words_ids = [model.tokenizer.encode(word) for word in ["Observation:", "Observation:\n"]]
        kwargs.update({"stop_words_ids": stop_words_ids})

    response, extra = model.chat(request.messages, stream=request.stream, **kwargs)
    if request.stream:
        predict = _predict(model.id, response, extra, with_function_call)
        return EventSourceResponse(predict, media_type="text/event-stream")
    else:
        finish_reason = "stop"

        if with_function_call:
            message, finish_reason = build_chat_message(response)
        else:
            message=ChatMessage(role="assistant", content=response)

        choice_data = ChatCompletionResponseChoice( index=0, message=message, finish_reason=finish_reason)
        # FIXME: usage
        usage = UsageInfo()
        return ChatCompletionResponse(model=model.id, choices=[choice_data], object="chat.completion", usage=usage)


def _predict(model_id: str, generate, stream_type: str, with_function_call: bool = False):
    yield _compose_chunk(model_id, DeltaMessage(role="assistant"))
    current_length = 0
    total_response = ""
    found_action_name = False
    finish_reason = "stop"
    for response in generate:
        if stream_type == "delta":
            delta = response
            delta = delta[:-4] if delta.endswith("</s>") else delta
        else:
            if stream_type == "tuple":
                new_response, _ = response
            elif stream_type == "string":
                new_response = response

            if len(new_response) == current_length:
                continue
            delta = new_response[current_length:]
            current_length = len(new_response)
        total_response += delta

        if with_function_call:
            if found_action_name:
                # FIXME: do not return \nObservation:
                yield _compose_chunk(model_id, build_fc_args_message(delta))
                continue
            else:
                if total_response.rfind("\nFinal Answer:") > 0:
                    with_function_call = False
                if total_response.rfind("\nAction Input:") == -1:
                    continue
                else:
                    yield _compose_chunk(model_id, build_fc_name_message(total_response))
                    pos = total_response.rfind("\nAction Input:") + len("\nAction Input:")
                    yield _compose_chunk(model_id, build_fc_args_message(total_response[pos:]))
                    found_action_name = True
                    finish_reason = "function_call"
        else:
            yield _compose_chunk(model_id, DeltaMessage(content=delta))

    yield _compose_chunk(model_id, DeltaMessage(), finish_reason)
    yield '[DONE]'


def _compose_chunk(model_id: str, message: DeltaMessage, finish_reason: Optional[str] = None):
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=message,
        finish_reason=finish_reason
    )
    chunk = ChatCompletionResponse(model=model_id, choices=[choice_data], object="chat.completion.chunk")

    return "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False))

def _gen_kwargs(request: ChatCompletionRequest, tokenizer):
    kwargs = {}
    # stop_words_ids
    if request.stop is not None:
        kwargs["stop_words_ids"] = [tokenizer.encode(word) for word in request.stop]

    return kwargs