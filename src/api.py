import gc
import os
import torch

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .llms import get_model as get_llm_model
from .diffusers import get_model as get_diffuser_model
from .audios import get_model as get_audio_model

from .routes.audio import audio_router
from .routes.chat import chat_router
from .routes.embedding import embedding_router
from .routes.file import file_router
from .routes.finetune import fine_tune_router
from .routes.image import image_router
from .routes.models import models_router

from .utils.env import get_preload_models
from .utils.logger import get_logger
from .utils.cors import add_cors_middleware

load_dotenv()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    yield

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    if torch.backends.mps.is_available():
        torch.mps.empty_cache()

api = FastAPI(lifespan=lifespan)

add_cors_middleware(api)


@api.on_event("startup")
async def startup_event():
    print("Starting up...")

prefix = os.environ.get('API_PREFIX', "/api/v1")
api.include_router(audio_router, prefix=prefix, tags=["Audio"])
api.include_router(chat_router, prefix=prefix, tags=["Chat"])
api.include_router(embedding_router, prefix=prefix, tags=["Embedding"])
api.include_router(file_router, prefix=prefix, tags=["File"])
api.include_router(fine_tune_router, prefix=prefix, tags=["FineTune"])
api.include_router(models_router, prefix=prefix, tags=["Model"])
api.include_router(image_router, prefix=prefix, tags=["Image"])

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "/tmp/openai.mini/images")
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
api.mount("/images", StaticFiles(directory=IMAGE_FOLDER), name="images")
api.mount("/", StaticFiles(directory="./web"), name="homepage")


@api.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@api.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})


if __name__ == '__main__':
    preload_llms = get_preload_models("LLMS_PRELOAD")
    print("preloading models:", preload_llms)
    for name in preload_llms:
        get_llm_model(name)

    preload_diffusers = get_preload_models("DIFFUSERS_PRELOAD")
    print("preloading diffusers models:", preload_diffusers)
    for name in preload_diffusers:
        get_diffuser_model(name)

    preload_audios = get_preload_models("AUDIOS_PRELOAD")
    print("preloading audio models:", preload_audios)
    for name in preload_audios:
        get_audio_model(name)

    import uvicorn
    uvicorn.run("src.api:api",
                host=os.environ.get('SERVER_HOST', '0.0.0.0'),
                port=int(os.environ.get('SERVER_PORT', 8000)),
                # reload=True,
                workers=1)
