import torch
from threading import Thread
from transformers import TextIteratorStreamer
from typing import List, Optional

from .base import LlmModel
from src.utils.token import TokenFormatConfig, format_tokens
from src.type import ChatMessage

class LLaMA(LlmModel):
    def load(self):
        super().load()
        self.tokenizer.add_special_tokens({"pad_token": "<PAD>"})
        return self
    
    def chat(self, messages: List[str], stream: bool = False, token_format_config: Optional[TokenFormatConfig] = None, **kwargs):
        streamer = _stream_chat(self.model, self.tokenizer, messages, token_format_config) #, **kwargs)
        if stream:
            return streamer, "delta"
        else:
            chunks = []
            for chunk in streamer:
                chunks.append(chunk)

            return "".join(chunks).strip(), None


def _stream_chat(model, tokenizer, messages: List[ChatMessage], token_format_config: TokenFormatConfig = None, **kwargs):
    gen_kwargs = _compose_args(tokenizer, messages, token_format_config)

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    return gen_kwargs["streamer"]

def _compose_args(tokenizer, messages: List[ChatMessage], token_format_config: TokenFormatConfig = None):
    gen_kwargs = {"do_sample": True, "max_length": 2048, "temperature": 1.0,
                  "repetition_penalty": 1.2, "top_p": 0.95, "eos_token_id": tokenizer.eos_token_id}

    config = token_format_config if token_format_config is not None else TokenFormatConfig()
    chat = format_tokens(messages, tokenizer, config)
    input_ids = torch.tensor(chat).long()
    input_ids = input_ids.unsqueeze(0)
    input_ids = input_ids.to("cuda")
    gen_kwargs["input_ids"] = input_ids

    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs["streamer"] = streamer

    return gen_kwargs