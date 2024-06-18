from threading import Thread
from typing import List, Optional

import torch
from transformers import StoppingCriteriaList, StoppingCriteria, TextIteratorStreamer

from .base import LlmModel


class KeywordsStoppingCriteria(StoppingCriteria):
    def __init__(self, keywords_ids:list):
        self.keywords = []
        for keywords_id in keywords_ids:
            key_tensor = torch.tensor(keywords_id)
            key_tensor = key_tensor.to('cuda')
            self.keywords.append(key_tensor)

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for kw_id in self.keywords:
            if torch.equal(input_ids[0][-len(kw_id):], kw_id):
                return True
        return False


class Qwen2(LlmModel):

    def chat(self, messages: List[str], stream: Optional[bool] = False, **kwargs):
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to('cuda')

        if stream:
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
            generation_kwargs = dict(model_inputs, streamer=streamer, max_new_tokens=512)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            return streamer, self.stream_type
        else:
            if 'stop_words_ids' in kwargs:
                stop_ids = kwargs['stop_words_ids']
                generated_ids = self.model.generate(
                    model_inputs.input_ids,
                    stopping_criteria=StoppingCriteriaList([KeywordsStoppingCriteria(stop_ids)]),
                )
            else:
                generated_ids = self.model.generate(
                    model_inputs.input_ids,
                )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return response, None
