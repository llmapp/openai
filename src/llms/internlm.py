from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List

from .utils import seprate_messages
from ..type import ChatMessage


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).cuda()
    model.eval()

    return model, tokenizer


def chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.chat(tokenizer, query, history=history)


def stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = seprate_messages(messages)
    return model.stream_chat(tokenizer, query, history)
