import os
import torch
from dotenv import load_dotenv
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from typing import List

from ..type import ChatMessage

load_dotenv()

WEIGHTS_PATH = os.environ.get("LLAMA_WEIGHTS")


def _load_model(model_name: str):
    path = os.path.join(WEIGHTS_PATH, model_name)

    model = AutoModelForCausalLM.from_pretrained(path, device_map="cuda").eval()

    tokenizer = AutoTokenizer.from_pretrained(path, use_fast=False)
    tokenizer.add_special_tokens({"pad_token": "<PAD>"})
    return model, tokenizer


default_gen_kwargs = {"do_sample": True, "max_length": 2048,
                      "temperature": 1.0, "repetition_penalty": 1.2, "top_p": 0.95}


def _chat(model, tokenizer, messages: List[ChatMessage]):
    chat = format_tokens(messages, tokenizer)
    input_ids = torch.tensor(chat).long()
    input_ids = input_ids.unsqueeze(0)
    input_ids = input_ids.to("cuda")

    response = model.generate(input_ids, **default_gen_kwargs, eos_token_id=tokenizer.eos_token_id)
    generated = tokenizer.decode(response[0], skip_prompt=True, skip_special_tokens=True)
    generated = generated[len(chat):].strip()
    return generated, None


def _stream_chat(model, tokenizer, messages: List[ChatMessage]):
    gen_kwargs = {**default_gen_kwargs, "eos_token_id": tokenizer.eos_token_id}
    chat = format_tokens(messages, tokenizer)
    input_ids = torch.tensor(chat).long()
    input_ids = input_ids.unsqueeze(0)
    input_ids = input_ids.to("cuda")
    gen_kwargs["input_ids"] = input_ids.cuda()

    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs["streamer"] = streamer

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    return streamer, "delta"


HANDLERS = {"load": _load_model, "chat": _chat, "stream_chat": _stream_chat}


Dialog = List[ChatMessage]

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


def format_tokens(dialog, tokenizer):
    if dialog[0].role != "system":
        dialog = [ChatMessage(role="system", content=DEFAULT_SYSTEM_PROMPT)] + dialog
    dialog = [ChatMessage(role=dialog[1].role, content=B_SYS
                          + dialog[0].content
                          + E_SYS
                          + dialog[1].content)] + dialog[2:]
    assert all([msg.role == "user" for msg in dialog[::2]]) and all(
        [msg.role == "assistant" for msg in dialog[1::2]]
    ), (
        "model only supports 'system','user' and 'assistant' roles, "
        "starting with user and alternating (u/a/u/a/u...)"
    )
    dialog_tokens: List[int] = sum(
        [
            tokenizer.encode(
                f"{B_INST} {(prompt.content).strip()} {E_INST} {(answer.content).strip()} ",
            )
            for prompt, answer in zip(dialog[::2], dialog[1::2])
        ],
        [],
    )
    assert (
        dialog[-1].role == "user"
    ), f"Last message must be from user, got {dialog[-1].role}"
    dialog_tokens += tokenizer.encode(
        f"{B_INST} {(dialog[-1].content).strip()} {E_INST}",
    )

    return dialog_tokens
