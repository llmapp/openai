from transformers import AutoTokenizer, AutoModel
from typing import List

from .utils import seprate_messages
from ..type import ChatMessage


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
    if model_id == 'THUDM/chatglm-6b':
        model.half()
    model.cuda().eval()

    return model, tokenizer


def chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.chat(tokenizer, query, history=history)


def stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.stream_chat(tokenizer, query, history)
