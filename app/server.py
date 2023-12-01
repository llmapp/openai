import os

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


from .backend.plugin import plugin_router
from .backend.chat import chat_router


load_dotenv()


def add_cors_middleware(app):
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    print("Starting up...")
    yield
    print("Shutting down...")

api = FastAPI(lifespan=lifespan)

add_cors_middleware(api)


prefix = os.environ.get('API_PREFIX', "/api/v1")
api.include_router(plugin_router, prefix=prefix)
api.include_router(chat_router, prefix=prefix)

api.mount("/", StaticFiles(directory="./app/frontend/dist", html=True), name="homepage")


@api.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.server:api",
                host=os.environ.get('SERVER_HOST', '0.0.0.0'),
                port=int(os.environ.get('APP_PORT', 8001)),
                reload=True,
                workers=1)
