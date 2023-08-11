from typing import List, Optional

from .base import LlmModel, split_messages


class InternLM(LlmModel):
    # stop=["<|User|>", "<|Bot|>", "<eoa>"]
    def chat(self, messages: List[str], stream: Optional[bool] = False, **kwargs):
        if stream:
            query, history = split_messages(messages)
            response = self.model.stream_chat(self.tokenizer, query, history) #, **kwargs)
            return response, "tuple"
        else:
            return super().chat(messages, stream) #, **kwargs)
