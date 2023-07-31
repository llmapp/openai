import os
import soundfile
from uuid import uuid4
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from ..utils.env import compose_model_id


def _load_model(model_name: str):
    model_id = compose_model_id(model_name, "openai")

    processor = WhisperProcessor.from_pretrained(model_id)
    model = WhisperForConditionalGeneration.from_pretrained(model_id)
    model.config.forced_decoder_ids = None

    return model, processor


def _transcribe(file, model, processor, prompt: str = None):
    # FIXME: this is a temporary solution
    file_path = "/tmp/" + str(uuid4()) + ".audio"
    with open(file_path, "wb") as f:
        f.write(file)

    speech, sample_rate = soundfile.read(file_path)
    input_features = processor(speech, return_tensors="pt", sampling_rate=sample_rate).input_features
    outputs = model.generate(input_features)
    transcription = processor.batch_decode(outputs, skip_special_tokens=True)

    os.remove(file_path)

    return "".join(transcription)


HANDLERS = {
    "load": _load_model, "transcribe": _transcribe
}
