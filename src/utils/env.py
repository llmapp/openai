import os
from dotenv import load_dotenv

load_dotenv()


def get_preload_llms():
    names = os.environ.get("PRELOAD_LLMS")
    if names is None or names.strip() == "":
        return []

    return [name.strip() for name in names.split(",")]
