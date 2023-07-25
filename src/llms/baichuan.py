import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from typing import List

from ..type import ChatMessage
from ..utils.env import compose_model_id


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "baichuan-inc")
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained(model_id)

    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    msgs = [__chat_message_to_baichuan_message(m) for m in messages]
    response = model.chat(tokenizer, msgs)
    return response, None


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    msgs = [__chat_message_to_baichuan_message(m) for m in messages]
    response = model.chat(tokenizer, msgs, stream=True)
    return response, "string"


def __chat_message_to_baichuan_message(message: ChatMessage):
    return {
        "role": message.role if message.role == "assistant" else "user",  # "system" role is not supported by Baichuan
        "content": message.content
    }


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}
