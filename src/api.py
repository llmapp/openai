import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .routes.chat import chat_router
from .utils.logger import get_logger
from .utils.cors import add_cors_middleware

load_dotenv()


logger = get_logger(__name__)

api = FastAPI()
add_cors_middleware(api)

@api.on_event("startup")
async def startup_event():
    print("Starting up...")

prefix = os.environ['API_PREFIX']
api.include_router(chat_router, prefix=prefix, tags=["Chat"])

@api.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@api.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})
