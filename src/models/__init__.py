import torch
from fastapi import HTTPException

from .audio import AudioModel
from .embedding import EmbeddingModel
from .image import ImageModel
from .llm import Baichuan, ChatGLM, InternLM, LLaMA, Qwen, Xverse


_MODELS = [
    ChatGLM("THUDM/chatglm-6b"),
    ChatGLM("THUDM/chatglm2-6b"),
    ChatGLM("THUDM/chatglm3-6b"),
    InternLM("internlm/internlm-chat-7b"),
    InternLM("internlm/internlm-chat-7b-8k"),
    Baichuan("baichuan-inc/Baichuan-13B-Chat", model_args={"torch_dtype": torch.float16, "device_map": "auto"}),
    Baichuan("baichuan-inc/Baichuan2-13B-Chat", model_args={"torch_dtype": torch.bfloat16, "device_map": "auto"}),
    LLaMA("meta-llama/Llama-2-7b-chat-hf", model_args={"torch_dtype": torch.float16}),
    LLaMA("meta-llama/Llama-2-13b-chat-hf", model_args={"torch_dtype": torch.float16}),
    LLaMA("stabilityai/FreeWilly2", model_args={"torch_dtype": torch.float16, "low_cpu_mem_usage": True, "device_map": "auto"}),
    Qwen("Qwen/Qwen-7B-Chat", owner="Alibaba Cloud"),
    Qwen("Qwen/Qwen-14B-Chat", owner="Alibaba Cloud"),
    Xverse("xverse/XVERSE-13B-Chat", model_args={"torch_dtype": torch.bfloat16}),

    AudioModel("openai/whisper-large-v2"),
    AudioModel("openai/whisper-medium.en"),
    AudioModel("openai/whisper-tiny"),

    EmbeddingModel("BAAI/bge-large-zh", normalize_embeddings=True),
    EmbeddingModel("moka-ai/m3e-large"),
    EmbeddingModel("thenlper/gte-large"),
    EmbeddingModel("infloat/e5-large-v2"),
    EmbeddingModel("infloat/multilingual-e5-large"),

    ImageModel("stabilityai/stable-diffusion-xl-base-1.0"),
]
_LOADED_MODELS = {}


def get_model(model_id: str, skip_load: bool = False):
    if len(model_id.split("/")) > 2:
        raise HTTPException(status_code=400, detail=f"Invalid model id format {model_id}, should be <id> or <org>/<id> like gpt-3.5-turbo or openai/gpt-3.5-turbo")

    model = next((m for m in _MODELS if m.id == model_id or f"{m.org}/{m.id}" == model_id), None)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not supported!")

    if skip_load:
        return model

    real_id = model_id.split('/')[-1]
    loaded = _LOADED_MODELS.get(real_id)

    if loaded is None:
        model.load()
        loaded = model
        _LOADED_MODELS[model.id] = model

    return loaded

def list():
	global _MODELS
	return [m.to_card() for m in _MODELS]



