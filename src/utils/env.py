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
