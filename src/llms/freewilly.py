import torch
from typing import List

from .llama import HANDLERS as LLAMA_HANDLERS

from ..utils.token import TokenFormatConfig
from ..type import ChatMessage

_SYSTEM_PROMPT = "\
You are Free Willy, an AI that follows instructions extremely well. \
Help as much as you can. Remember, be safe, and don't do anything illegal."

_token_format_config = TokenFormatConfig(
    SYSTEM_PROMPT=_SYSTEM_PROMPT,
    B_SYS="### System:\n", E_SYS="\n\n",
    B_INST="### User:\n", E_INST="\n\n",
    B_AI="### Assistant:\n", E_AI="\n\n")

_ORGANIZATION = 'stabilityai'


def _load_model(model_name: str):
    extra_args = {"torch_dtype": torch.float16, "low_cpu_mem_usage": True, "device_map": "auto"}
    return LLAMA_HANDLERS.get("load")(model_name, _ORGANIZATION, extra_args)


def _chat(model, tokenizer, messages: List[ChatMessage]):
    return LLAMA_HANDLERS.get("chat")(model, tokenizer, messages, _token_format_config)


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    return LLAMA_HANDLERS.get("stream_chat")(model, tokenizer, messages, _token_format_config)


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}
