import os
import soundfile
import torch
from uuid import uuid4
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration

from ..utils.env import compose_model_id


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "openai")

    # FIXME: the model are loaded twice

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_id,
        chunk_length_s=30,
        device="cuda:0" if torch.cuda.is_available() else "cpu",
    )

    processor = WhisperProcessor.from_pretrained(model_id)
    model = WhisperForConditionalGeneration.from_pretrained(model_id)
    model.config.forced_decoder_ids = None

    return model, processor, pipe


def _transcribe(audio, model, **kwargs):
    # FIXME: this is a temporary solution
    file_path = "/tmp/" + str(uuid4()) + ".audio"
    with open(file_path, "wb") as f:
        f.write(audio)

    speech, _ = soundfile.read(file_path)
    input_features = model.processor(speech, return_tensors="pt", sampling_rate=16000).input_features
    outputs = model.model.generate(input_features, **kwargs)
    transcription = model.processor.batch_decode(outputs, skip_special_tokens=True)

    os.remove(file_path)

    return "".join(transcription)


def _translate(audio, model, **kwargs):
    # FIXME: this is a temporary solution
    file_path = "/tmp/" + str(uuid4()) + ".audio"
    with open(file_path, "wb") as f:
        f.write(audio)

    speech, _ = soundfile.read(file_path)
    translation = model.pipe(speech.copy(), batch_size=8, generate_kwargs={"task": "translate", **kwargs})["text"]

    os.remove(file_path)

    return "".join(translation)


HANDLERS = {
    "load": _load_model, "transcribe": _transcribe, "translate": _translate
}
