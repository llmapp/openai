from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List

from ..utils.message import split_messages
from ..utils.env import compose_model_id

from ..type import ChatMessage


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "internlm")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cuda", trust_remote_code=True).cuda()
    model.eval()

    return model, tokenizer


# stop=["<|User|>", "<|Bot|>", "<eoa>"]

def _chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = split_messages(messages)
    return model.chat(tokenizer, query, history=history)


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = split_messages(messages)
    return model.stream_chat(tokenizer, query, history=history), "tuple"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}
