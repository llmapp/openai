import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def get_preload_models(env_name: str):
    names = os.environ.get(env_name)
    if names is None or names.strip() == "":
        return []

    return [name.strip() for name in names.split(",")]


MODEL_HUB_PATH = os.environ.get("MODEL_HUB_PATH", "models")


def compose_model_id(model_name: str, prefix: str, suffix: Optional[str] = None, remove_prefix: bool = False, ):
    model_id = model_name if model_name.startswith(prefix + "/") else prefix + "/" + model_name

    path = os.path.join(MODEL_HUB_PATH, model_id)
    path = path + suffix if suffix is not None else path
    if os.path.exists(path):
        model_id = path
    else:
        model_id = model_id[len(prefix) + 1:] if remove_prefix else model_id

    return model_id
