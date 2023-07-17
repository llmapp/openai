import os

from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any, List

from .baichuan import HANDLERS as BAICHUAN_HANDLERS
from .chatglm import HANDLERS as CHATGLM_HANDLERS
from .internlm import HANDLERS as INTERNLM_HANDLERS


models = {
    "chatglm-6b": CHATGLM_HANDLERS,
    "chatglm2-6b": CHATGLM_HANDLERS,
    "internlm-chat-7b": INTERNLM_HANDLERS,
    "internlm-chat-7b-8k": INTERNLM_HANDLERS,
    "Baichuan-13B-Chat": BAICHUAN_HANDLERS,
}

load_dotenv()
LLMS_DISABLED = os.environ.get("LLMS_DISABLED")
if LLMS_DISABLED is not None and LLMS_DISABLED.strip() != "":
    for name in [name.strip() for name in LLMS_DISABLED.split(",")]:
        if name in models:
            del models[name]


class LLM(BaseModel):
    id: str
    tokenizer: Any
    model: Any


def get_models():
    return list(models.keys())


llms: List[LLM] = []


def get_model(model_id: str):
    global llms

    if models.get(model_id) is None:
        raise ValueError(f"Model {model_id} not found")

    llm = next((l for l in llms if l.id == model_id), None)

    if llm is None:
        handlers = models.get(model_id)
        model, tokenizer = handlers.get("load")(model_id)

        llm = LLM(id=model_id, tokenizer=tokenizer, model=model)
        llms.append(llm)

    return llm.model, llm.tokenizer
