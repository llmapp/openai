from typing import List, Optional

from .base import LlmModel, split_messages

class Qwen(LlmModel):

    def chat(self, messages: List[str], stream: Optional[bool] = False, **kwargs):
        if stream:
            query, history = split_messages(messages)
            response = self.model.chat_stream(self.tokenizer, query, history, **kwargs)
            return response, self.stream_type
        else:
            return super().chat(messages, **kwargs)
