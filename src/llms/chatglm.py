from transformers import AutoTokenizer, AutoModel
from typing import List

from ..type import ChatCompletionResponse, ChatCompletionResponseStreamChoice, ChatMessage, DeltaMessage


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True).cuda()
    model.eval()

    return model, tokenizer


def chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = _seprate_messages(messages)

    return model.chat(tokenizer, query, history=history)


def stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = _seprate_messages(messages)
    return model.stream_chat(tokenizer, query, history)


def _seprate_messages(messages: List[ChatMessage]):
    query = messages[-1].content

    prev_messages = messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        query = prev_messages.pop(0).content + query

    history = []
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i+1].role == "assistant":
                history.append([prev_messages[i].content, prev_messages[i+1].content])

    return query, history
