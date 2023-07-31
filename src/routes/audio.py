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
                               temperature: Optional[float] = Form(1.0), language: Optional[str] = Form("zh")):
    audio_model = get_model(model)
    transcribe = models.get(model).get("transcribe")

    kwargs = {"prompt": prompt, "temperature": temperature, "language": language}
    text = transcribe(file, audio_model, **kwargs)

    if response_format == "json":
        return AudioResponse(text=text)
    else:
        raise NotImplementedError()


@audio_router.post("/translations", response_model=AudioResponse)
async def create_translation(file: bytes = File(...), model: str = Form(...), prompt: Optional[str] = Form(None),
                             response_format: Optional[str] = Form("json"), temperature: Optional[float] = Form(1.0)):
    audio_model = get_model(model)
    translate = models.get(model).get("translate")

    kwargs = {"prompt": prompt, "temperature": temperature, "language": "en"}
    text = translate(file, audio_model, **kwargs)

    if response_format == "json":
        return AudioResponse(text=text)
    else:
        raise NotImplementedError()
