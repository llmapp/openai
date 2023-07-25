import os
from dotenv import load_dotenv

load_dotenv()


def get_preload_llms():
    names = os.environ.get("LLMS_PRELOAD")
    if names is None or names.strip() == "":
        return []

    return [name.strip() for name in names.split(",")]


def get_preload_diffusers():
    names = os.environ.get("DIFFUSERS_PRELOAD")
    if names is None or names.strip() == "":
        return []

    return [name.strip() for name in names.split(",")]


MODEL_HUB_PATH = os.environ.get("MODEL_HUB_PATH", "models")


def compose_model_id(model_name: str, prefix: str):
    model_id = model_name if model_name.startswith(prefix) else prefix + "/" + model_name

    if os.path.exists(os.path.join(MODEL_HUB_PATH, model_id)):
        model_id = os.path.join(MODEL_HUB_PATH, model_id)

    return model_id
