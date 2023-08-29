from typing import List, Optional

from .base import LlmModel

from src.type import ChatMessage

class Xverse(LlmModel):
    def chat(self, messages: List[ChatMessage], stream: Optional[bool]=False, **kwargs):
        messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.model.chat(self.tokenizer, messages, stream=stream) #, **kwargs)
        if stream:
            return response, "delta"
        else:
            return response, None


