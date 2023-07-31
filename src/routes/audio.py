from fastapi import APIRouter, File, Form
from typing import Optional

from ..audios import models, get_model
from ..utils.logger import get_logger
from ..type import AudioResponse


audio_router = APIRouter(prefix="/audio")

logger = get_logger(__name__)


@audio_router.post("/transcriptions", response_model=AudioResponse)
async def create_transcription(file: bytes = File(...), model: str = Form(...),
                               prompt: Optional[str] = Form(None), response_format: Optional[str] = Form("json"),
                               temperature: Optional[float] = Form(1.0), language: Optional[str] = Form("en")):
    logger.info(f"Request: {model}")

    audio_model = get_model(model)
    transcribe = models.get(model).get("transcribe")

#     logger.info(f"Prompt: {prompt}")

    text = transcribe(file, audio_model.model, audio_model.processor, prompt)
    # text = "Hello world!"
    response = AudioResponse(text=text)
    return response


@audio_router.post("/translations", response_model=AudioResponse)
async def create_translation(file: bytes = File(...), model: str = Form(...), prompt: Optional[str] = Form(None),
                             response_format: Optional[str] = Form("json"), temperature: Optional[float] = Form(1.0)):
    pass
