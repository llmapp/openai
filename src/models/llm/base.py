from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation import GenerationConfig
from typing import Any, List, Literal, Optional

from ..base import Model
from src.utils.env import compose_model_id
from src.type import ChatMessage, ChatFunction

StreamType = Literal["tuple", "string"]

class LlmModel(Model):
    model: Any
    tokenizer: Any

    stream_type: StreamType = "string"
    model_args: dict
    tokenizer_args: dict
    generation_config: dict

    def __init__(self, model: str, name: Optional[str]=None, owner: Optional[str]=None, stream_type: Optional[StreamType]='string', model_args: Optional[dict]={}, tokenizer_args: Optional[dict]={}, generation_config: Optional[dict]={}):
        super().__init__(model, name, owner)
        self.stream_type = stream_type

        default_tokenizer_args = { "use_fast": False, "trust_remote_code": True }
        default_model_args = { "device_map": "cuda", "trust_remote_code": True }
        default_generation_config = { "trust_remote_code": True }

        self.model_args = {**default_model_args, **model_args}
        self.tokenizer_args = {**default_tokenizer_args, **tokenizer_args}
        self.generation_config = {**default_generation_config, **generation_config}


    def load(self):
        model_id = compose_model_id(self.id, prefix=self.org)
        print(f"Loading model {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, **self.tokenizer_args)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, **self.model_args)
        self.model.eval()
        self.model.generation_config = GenerationConfig.from_pretrained(model_id, **self.generation_config)
        print(f"Model {model_id} loaded!")

        return self


    def chat(self, messages: List[ChatMessage], functions: Optional[List[ChatFunction]] = None, stream: Optional[bool] = False, **kwargs):
        query, history = split_messages(messages)
        if stream:
            response = self.model.chat(self.tokenizer, query, history=history, functions=functions, stream=True) #, **kwargs)
            return response, self.stream_type
        else:
            return self.model.chat(self.tokenizer, query, history=history, functions=functions) #, **kwargs)



def split_messages(messages: List[ChatMessage]):
    query = messages[-1].content

    prev_messages = messages[:-1]
    if len(prev_messages) > 0 and prev_messages[0].role == "system":
        query = prev_messages.pop(0).content + query

    history = []
    if len(prev_messages) % 2 == 0:
        for i in range(0, len(prev_messages), 2):
            if prev_messages[i].role == "user" and prev_messages[i+1].role == "assistant":
                history.append([prev_messages[i].content, prev_messages[i+1].content])

    return query, history
