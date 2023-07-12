import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained(model_id)

    return model, tokenizer
