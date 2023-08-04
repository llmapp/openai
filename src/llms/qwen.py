from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation import GenerationConfig
from typing import List

from ..utils.message import split_messages
from ..utils.env import compose_model_id

from ..type import ChatMessage


_ORGANIZATION = 'Qwen'


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, prefix=_ORGANIZATION)
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, device_map="cuda", trust_remote_code=True, fp16=True).cuda().eval()
    model.generation_config = GenerationConfig.from_pretrained(model_id, trust_remote_code=True)

    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = split_messages(messages)
    return model.chat(tokenizer, query, history=history)


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    query, history = split_messages(messages)
    response = model.chat(tokenizer, query, history, stream=True)
    return response, "string"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}
