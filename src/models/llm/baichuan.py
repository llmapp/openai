from typing import List, Optional

from .base import LlmModel

from src.type import ChatMessage

class Baichuan(LlmModel):
    def chat(self, messages: List[ChatMessage], stream: Optional[bool]=False, **kwargs):
        msgs = [_chat_message_to_baichuan_message(m) for m in messages]
        response = self.model.chat(self.tokenizer, msgs, stream=stream) #, **kwargs)
        if stream:
            return response, "string"
        else:
            return response, None


def _chat_message_to_baichuan_message(message: ChatMessage):
    return {
        "role": message.role if message.role == "assistant" else "user",  # "system" role is not supported by Baichuan
        "content": message.content
    }