from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Optional

from src.utils.env import compose_model_id

from .base import LlmModel, split_messages

class Qwen(LlmModel):
    def load(self):
        model_id = compose_model_id(self.id, prefix=self.org)
        print(f"Loading model {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, **self.tokenizer_args)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, **self.model_args)
        if 'fp16' in self.model_args:
            self.model.bfloat16().eval()
        else:
            self.model.eval()
        print(f"Model {model_id} loaded!")

        return self

    def chat(self, messages: List[str], stream: Optional[bool] = False, **kwargs):
        query, history = split_messages(messages)
        if stream:
            response = self.model.chat_stream(self.tokenizer, query, history, **kwargs)
            return response, self.stream_type
        else:
            response = self.model.chat(self.tokenizer, query, history, **kwargs)
            return response
