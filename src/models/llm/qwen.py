from typing import List, Optional

from .base import LlmModel, split_messages
from src.utils.function_call import need_function_call, build_function_call_message

class Qwen(LlmModel):

    def chat(self, messages: List[str], functions: Optional[any] = None, stream: Optional[bool] = False, **kwargs):
        query, history = split_messages(messages)
        need = need_function_call(messages, functions)
        if need:
            last = build_function_call_message(messages, functions)
            query = last.content
            stop_words_ids = [self.tokenizer.encode(word) for word in ["Observation:", "Observation:\n"]]
            kwargs.update({"stop_words_ids": stop_words_ids})

        if stream:
            response = self.model.chat_stream(self.tokenizer, query, history, **kwargs)
            return response, self.stream_type
        else:
            response = self.model.chat(self.tokenizer, query, history, **kwargs)
            return response
