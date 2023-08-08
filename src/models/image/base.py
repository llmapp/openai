import torch
from diffusers import DiffusionPipeline
from typing import Any

from src.utils.env import compose_model_id
from ..base import Model


class ImageModel(Model):
    pipeline: Any

    def load(self):
        model_id = compose_model_id(self.id, prefix=self.org)
        print(f"Loading model {model_id}")
        self.pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        self.pipeline.to("cuda")
        print(f"Model {model_id} loaded!")

        return self

    def generate(self, **kwargs):
        return self.pipeline(**kwargs).images
