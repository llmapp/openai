from fastapi import APIRouter, Form, UploadFile
from typing import Optional, Literal

from ..models import get_model
from ..models.audio import AudioModel

from ..utils.logger import get_logger
from ..utils.request import raise_if_invalid_model
from ..type import AudioResponse


audio_router = APIRouter(prefix="/audio")

logger = get_logger(__name__)


@audio_router.post("/transcriptions", response_model=AudioResponse)
async def create_transcription(file: UploadFile, model: str = Form(...),
                               prompt: Optional[str] = Form(None), response_format: Optional[str] = Form("json"),
                               temperature: Optional[float] = Form(1.0), language: Optional[str] = Form("zh")):
    kwargs = {"language": language, "initial_prompt": prompt, "temperature": temperature}
    return _do_transform("transcribe", file, model, response_format, kwargs)


@audio_router.post("/translations", response_model=AudioResponse)
async def create_translation(file: UploadFile, model: str = Form(...),
                             prompt: Optional[str] = Form(None), response_format: Optional[str] = Form("json"),
                             temperature: Optional[float] = Form(1.0), language: Optional[str] = Form("en")):
    kwargs = {"language": language, "initial_prompt": prompt, "temperature": temperature}
    return _do_transform("translate", file, model, response_format, kwargs)


def _do_transform(type: Literal['translate', 'transcribe'], file: UploadFile, model, response_format, kwargs):
    audio_model = get_model(model)
    raise_if_invalid_model(audio_model, AudioModel)

    runner = audio_model.transcribe if type == "transcribe" else audio_model.translate
    # audio_model = get_model(model)
    # result = runner(file.file, audio_model, kwargs)
    result = runner(file.file, **kwargs)

    if response_format == "json":
        return AudioResponse(text=result["text"])
    else:
        raise NotImplementedError()
