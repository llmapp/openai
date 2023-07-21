import os
import torch
from dotenv import load_dotenv
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from transformers.generation.utils import GenerationConfig
from typing import List

from ..type import ChatMessage

load_dotenv()

WEIGHTS_PATH = os.environ.get("LLAMA_WEIGHTS")


def _load_model(model_name: str):
    path = os.path.join(WEIGHTS_PATH, model_name)
    tokenizer = AutoTokenizer.from_pretrained(path, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(path, device_map="cuda", trust_remote_code=True).eval()
    model.generation_config = GenerationConfig.from_pretrained(path)
    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    ctx = _messages_to_ctx(messages)
    ctx += "\nassistant: "
    input_ids = tokenizer.encode(ctx, return_tensors="pt")
    response = model.generate(input_ids.cuda(),
                              do_sample=True,
                              max_length=2048,
                              temperature=1.0,
                              repetition_penalty=1.2,
                              eos_token_id=tokenizer.eos_token_id)
    generated = tokenizer.decode(response[0])
    text = generated[len(ctx) + len('<s>'):].strip()
    text = text[:text.find('</s>')].strip()
    return text, None


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    gen_kwargs = {"do_sample": True, "max_length": 2048, "temperature": 1.0,
                  "repetition_penalty": 1.2, "top_p": 0.95, "eos_token_id": tokenizer.eos_token_id}

    ctx = _messages_to_ctx(messages)
    ctx += "\nassistant: "
    input_ids = tokenizer.encode(ctx, return_tensors="pt")
    gen_kwargs["input_ids"] = input_ids.cuda()

    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True)
    gen_kwargs["streamer"] = streamer

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    return streamer, "delta"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}


def _messages_to_ctx(messages: List[ChatMessage]):
    ctx = """"\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""
    for message in messages:
        ctx += "\n" + _message_to_ctx(message)
    ctx = (ctx[-1920:]) if len(ctx) >= 2048 else ctx
    return ctx


def _message_to_ctx(message: ChatMessage):
    return message.role + ": " + message.content
