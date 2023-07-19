from transformers import AutoTokenizer, AutoModel
from typing import List

from .utils import seprate_messages
from ..type import ChatMessage

MODEL_PREFIX = "THUDM/"


def _load_model(model_name: str):
    model_id = model_name if model_name.startswith(MODEL_PREFIX) else MODEL_PREFIX + model_name
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True)

    if model_name == 'chatglm-6b':
        model.half()

    model.cuda().eval()

    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.chat(tokenizer, query, history=history)


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.stream_chat(tokenizer, query, history), "tuple"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}
