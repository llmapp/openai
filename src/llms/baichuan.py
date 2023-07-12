import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from typing import List

from ..type import ChatMessage


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained(model_id)

    return model, tokenizer


def chat(model, tokenizer, messages: List[ChatMessage]):
    msgs = [_chat_message_to_baichuan_message(m) for m in messages]
    response = model.chat(tokenizer, msgs)
    return response, None


# TODO: Implement this
def stream_chat(model, tokenizer, messages: List[ChatMessage]):
    raise NotImplementedError()


def _chat_message_to_baichuan_message(message: ChatMessage):
    return {
        "role": message.role if message.role == "assistant" else "user",  # "system" role is not supported by Baichuan
        "content": message.content
    }
