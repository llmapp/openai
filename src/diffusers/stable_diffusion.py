from diffusers import DiffusionPipeline
import torch

from ..utils.logger import get_logger
from ..utils.env import compose_model_id

logger = get_logger(__name__)


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "stabilityai")

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
