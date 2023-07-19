import os
import torch
from dotenv import load_dotenv
from threading import Thread
from transformers import LlamaForCausalLM, LlamaTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
from typing import List

from ..type import ChatMessage

load_dotenv()

WEIGHTS_PATH = os.environ.get("LLAMA_WEIGHTS")


def _load_model(model_name: str):
    path = os.path.join(WEIGHTS_PATH, model_name)
    tokenizer = LlamaTokenizer.from_pretrained(path)
    model = LlamaForCausalLM.from_pretrained(path)
    return model, tokenizer


def _chat(model, tokenizer, messages: List[ChatMessage]):
    ctx = _messages_to_ctx(messages)
    ctx += "\nAI: "
    input_ids = tokenizer.encode(ctx, return_tensors="pt")
    stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub()])
    response = model.generate(input_ids,
                              do_sample=True,
                              top_k=50,
                              max_length=2048,
                              top_p=0.95,
                              temperature=1.0,
                              stopping_criteria=stopping_criteria)
    generated = tokenizer.decode(response[0])
    return generated[len(ctx) + len('<s>'):].strip(), None


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    gen_kwargs = {"max_length": 2048, "temperature": 1.0, "top_p": 0.95}

    ctx = _messages_to_ctx(messages)
    ctx += "\nAI: "
    input_ids = tokenizer.encode(ctx, return_tensors="pt")
    gen_kwargs["input_ids"] = input_ids

    stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub()])
    gen_kwargs["stopping_criteria"] = stopping_criteria

    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs["streamer"] = streamer

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    return streamer, "delta"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}


class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self):
        super().__init__()

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, stops=[]):
        # FIXME: Only one line is generated
        if input_ids[0][-1] == 13:
            return True
        return False


def _messages_to_ctx(messages: List[ChatMessage]):
    ctx = "A dialog, where User interacts with AI. AI is helpful, kind, obedient, honest, and knows its own limits."
    for message in messages:
        ctx += "\n" + _message_to_ctx(message)
    ctx = (ctx[-1920:]) if len(ctx) >= 2048 else ctx
    return ctx


def _message_to_ctx(message: ChatMessage):
    return ("AI" if message.role == 'assistant' else message.role) + ": " + message.content
