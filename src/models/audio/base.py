import os
import tempfile
import whisper
from typing import Any
from uuid import uuid4

from src.utils.env import compose_model_id
from ..base import Model


class AudioModel(Model):
    model: Any

    
    def load(self):
        model_name = self.id[len("whisper-"):]
        model_id = compose_model_id(model_name, prefix=self.org, suffix=".pt", remove_prefix=True)
        print(f"Loading model {model_id}")
        self.model = whisper.load_model(model_id)
        print(f"Model {model_id} loaded!")
        return self


    def transcribe(self, file, **kwargs):
        audio = _convert_audio(file)
        return self.model.transcribe(audio, task="transcribe", **kwargs)


    def translate(self, file, **kwargs):
        audio = _convert_audio(file)
        return self.model.transcribe(audio, task="translation", **kwargs)


def _convert_audio(audio):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, f"{uuid4()}.audio")
        with open(path, "wb") as f:
            f.write(audio.read())
        waveform = whisper.load_audio(path)
        os.remove(path)
    return waveform
