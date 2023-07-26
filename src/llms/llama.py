import torch
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from typing import List

from ..utils.token import TokenFormatConfig, format_tokens
from ..utils.env import compose_model_id

from ..type import ChatMessage


token_format_config = TokenFormatConfig()


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "meta-llama")
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cuda").eval()  # , torch_dtype=torch.float16

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
    tokenizer.add_special_tokens({"pad_token": "<PAD>"})
    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    streamer, _ = _stream_chat(model, tokenizer, messages)

    chunks = []
    for chunk in streamer:
        chunks.append(chunk)

    return "".join(chunks).strip(), None


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    gen_kwargs = _compose_args(tokenizer, messages)

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    return gen_kwargs["streamer"], "delta"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}


def _compose_args(tokenizer, messages: List[ChatMessage]):
    gen_kwargs = {"do_sample": True, "max_length": 2048, "temperature": 1.0, "repetition_penalty": 1.2, "top_p": 0.95}
    gen_kwargs["eos_token_id"] = tokenizer.eos_token_id

    chat = format_tokens(messages, tokenizer, token_format_config)
    input_ids = torch.tensor(chat).long()
    input_ids = input_ids.unsqueeze(0)
    input_ids = input_ids.to("cuda")
    gen_kwargs["input_ids"] = input_ids

    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs["streamer"] = streamer

    return gen_kwargs
