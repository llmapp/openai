import os
import torch

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer, AutoModel

from .routes.chat import chat_router
from .routes.models import models_router
from .utils.logger import get_logger
from .utils.cors import add_cors_middleware

load_dotenv()


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI): # collects GPU memory
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

api = FastAPI(lifespan=lifespan)

add_cors_middleware(api)

@api.on_event("startup")
async def startup_event():
    print("Starting up...")

prefix = os.environ['API_PREFIX']
api.include_router(chat_router, prefix=prefix, tags=["Chat"])
api.include_router(models_router, prefix=prefix, tags=["Models"])

@api.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@api.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})

if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).cuda()
    model.eval()

    import uvicorn
    uvicorn.run(api, host='0.0.0.0', port=8000, workers=1)
