import os
import tempfile
import whisper
from uuid import uuid4

from ..utils.env import compose_model_id

_ORGANIAZTION = "openai"


def _load_model(model_name: str):
    model_name = model_name[len("whisper-"):]
    model_id = compose_model_id(model_name, prefix=_ORGANIAZTION, suffix=".pt", remove_prefix=True)
    download_root = os.path.join(os.environ.get("MODEL_HUB_PATH", "models"), _ORGANIAZTION)
    model = whisper.load_model(model_id, download_root=download_root)
    return model


def _transcribe(file, audio_model, kwargs):
    audio = _convert_audio(file)
    return audio_model.model.transcribe(audio, task="transcribe", **kwargs)


def _translate(file, audio_model, kwargs):
    audio = _convert_audio(file)
    return audio_model.model.transcribe(audio, task="translation", **kwargs)


def _convert_audio(file):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = f"{tmpdir}/{uuid4()}.audio"
        with open(path, "wb") as f:
            f.write(file.read())
        waveform = whisper.load_audio(path)
        waveform = whisper.pad_or_trim(waveform)
        os.remove(path)

    return waveform


HANDLERS = {
    "load": _load_model, "transcribe": _transcribe, "translate": _translate
}
