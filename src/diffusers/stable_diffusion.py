from diffusers import DiffusionPipeline
import torch

from ..utils.logger import get_logger

MODEL_PREFIX = "stabilityai/"

logger = get_logger(__name__)


def _load_model(model_name: str):
    model_id = model_name if model_name.startswith(MODEL_PREFIX) else MODEL_PREFIX + model_name

    logger.info(f"Loading model {model_id} ...")
    pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16,
                                             use_safetensors=True, variant="fp16")
    pipe.to("cuda")
    # pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)

    logger.info(f"Model {model_id} loaded!")

    return pipe


HANDLERS = {
    "load": _load_model,
}
