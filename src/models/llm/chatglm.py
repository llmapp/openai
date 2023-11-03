from transformers import AutoTokenizer, AutoModel
from typing import List, Optional

from src.utils.env import compose_model_id

from .base import LlmModel, split_messages
from ...type import ChatMessage


class ChatGLM(LlmModel):
    def load(self):
        model_id = compose_model_id(self.id, prefix=self.org)
        print(f"Loading model {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_id, device_map="cuda", trust_remote_code=True)
        if self.id == 'chatglm-6b':
            self.model.half()
        self.model.cuda().eval()
        print(f"Model {model_id} loaded!")

        return self

    def chat(self, messages: List[ChatMessage], stream: Optional[bool] = False, **kwargs):
        if stream:
            # ChatGLM3 uses a different chat format
            # ref: https://github.com/THUDM/ChatGLM3/blob/main/PROMPT_en.md
            if self.id == 'chatglm3-6b':
                query, history = messages[-1].content,messages[:-1]
                history = [{'role': h.role, 'content': h.content} for h in history]
            else:
                query, history = split_messages(messages)
            response = self.model.stream_chat(self.tokenizer, query, history) #, **kwargs)
            return response, "tuple"
        else:
            return super().chat(messages, stream=stream)  # , **kwargs)
