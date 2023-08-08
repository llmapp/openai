#  [WIP] OpenAI.mini

This repo implements OpenAI APIs with open source models, for example, open source LLMs for [chat](https://platform.openai.com/docs/api-reference/chat), `Whisper` for [audio](https://platform.openai.com/docs/api-reference/audio), `SDXL` for [image](https://platform.openai.com/docs/api-reference/images), `intfloat/e5-large-v2` for [embeddings](https://platform.openai.com/docs/api-reference/embeddings), and so on. With this repo, you can interact with LLMs using the [`openai` libraries](https://platform.openai.com/docs/api-reference) or the [`LangChain`](https://python.langchain.com/) library.

## Development

### Install dependencies

- `make install`

Start development server with the following command:

- `cp .env.example .env`, and modify the `.env` file on your need
- `make run`

Notice: the models can be loadded on startup or on the fly.

## Status

| Services          | API                      | Status           | Description             |
| :-----------------| :------------------------------------------------------------------------------------------------------| :----------------| :-----------------------|
| Authorization     |                                                                                                        |                  |                         |
| Models            | [List models](https://platform.openai.com/docs/api-reference/models/list)                              | ✅ Done          |                         |
| Models            | [Retrieve model](https://platform.openai.com/docs/api-reference/models/retrieve)                       |                  |                         |
| Chat              | [Create chat completion](https://platform.openai.com/docs/api-reference/chat/create)                   | Partial Done     | Support Multi. LLMs     |
| Completions       | [Create completion](https://platform.openai.com/docs/api-reference/completions/create)                 |                  |                         |
| Images            | [Create image](https://platform.openai.com/docs/api-reference/images/create)                           | ✅ Done          |                         |
| Images            | [Create image edit](https://platform.openai.com/docs/api-reference/images/create-edit)                 |                  |                         |
| Images            | [Create image variation](https://platform.openai.com/docs/api-reference/images/create-variation)       |                  |                         |
| Embeddings        | [Create embeddings](https://platform.openai.com/docs/api-reference/embeddings/create)                  | ✅ Done          | Support Multi. LLMs     |
| Audio             | [Create transcription](https://platform.openai.com/docs/api-reference/audio/create-transcription)      | ✅ Done          |                         |
| Audio             | [Create translation](https://platform.openai.com/docs/api-reference/audio/create-translation)          | ✅ Done          |                         |
| Files             | [List files](https://platform.openai.com/docs/api-reference/files/list)                                | ✅ Done          |                         |
| Files             | [Upload file](https://platform.openai.com/docs/api-reference/files/upload)                             | ✅ Done          |                         |
| Files             | [Delete file](https://platform.openai.com/docs/api-reference/files/delete)                             | ✅ Done          |                         |
| Files             | [Retrieve file](https://platform.openai.com/docs/api-reference/files/retrieve)                         | ✅ Done          |                         |
| Files             | [Retrieve file content](https://platform.openai.com/docs/api-reference/files/retrieve-content)         | ✅ Done          |                         |
| Fine-tunes        | [Create fine-tune](https://platform.openai.com/docs/api-reference/fine-tunes/create)                   |                  |                         |
| Fine-tunes        | [List fine-tunes](https://platform.openai.com/docs/api-reference/fine-tunes/list)                      |                  |                         |
| Fine-tunes        | [Retrieve fine-tune](https://platform.openai.com/docs/api-reference/fine-tunes/retrieve)               |                  |                         |
| Fine-tunes        | [Cancel fine-tune](https://platform.openai.com/docs/api-reference/fine-tunes/cancel)                   |                  |                         |
| Fine-tunes        | [List fine-tune events](https://platform.openai.com/docs/api-reference/fine-tunes/events)              |                  |                         |
| Fine-tunes        | [Delete fine-tune model](https://platform.openai.com/docs/api-reference/fine-tunes/delete-model)       |                  |                         |
| Moderations       | [Create moderation](https://platform.openai.com/docs/api-reference/moderations/create)                 |                  |                         |
| Edits             | [Create edit](https://platform.openai.com/docs/api-reference/edits/create)                             |                  |                         |

## Supported Language Models

| Model                                                                                 | #Params | Checkpoint link                                                                         |
| :------------------------------------------------------------------------------------ | :------ | :-------------------------------------------------------------------------------------- |
| [FreeWilly2](https://stability.ai/blog/freewilly-large-instruction-fine-tuned-models) | 70B     | [stabilityai/FreeWilly2](https://huggingface.co/stabilityai/FreeWilly2)                 |
| [Baichuan-13B-Chat](https://github.com/baichuan-inc/Baichuan-13B)                     | 13B     | [baichuan-inc/Baichuan-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat) |
| [Llama-2-13b-chat-hf](https://github.com/facebookresearch/llama)                      | 13B     | [meta-llama/Llama-2-13b-chat-hf](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf) |
| [Llama-2-7b-chat-hf](https://github.com/facebookresearch/llama)                       | 7B      | [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)   |
| [Qwen-7B-Chat](https://github.com/QwenLM/Qwen-7B) | 7B     | [Qwen/Qwen-7B-Chat](https://huggingface.co/Qwen/Qwen-7B-Chat)                 |
| [internlm-chat-7b](https://github.com/InternLM/InternLM)                              | 7B      | [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b)           |
| [chatglm2-6b](https://github.com/THUDM/ChatGLM2-6B)                                   | 6B      | [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)                           |
| [chatglm-6b](https://github.com/THUDM/ChatGLM-6B)                                     | 6B      | [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)                             |

## Supported Embedding Models

| Model                                                                                 | Embedding Dim.| Sequnce Length | Checkpoint link                                                                         |
| :------------------------------------------------------------------------------------ | :------ | :----- | :-------------------------------------------------------------------------------------- |
| [gte-large](https://huggingface.co/thenlper/gte-large) | 1024     | 512 | [thenlper/gte-large](https://huggingface.co/thenlper/gte-large)                 |
| [e5-large-v2](https://huggingface.co/intfloat/e5-large-v2) | 1024     | 512 | [intfloat/e5-large-v2](https://huggingface.co/intfloat/e5-large-v2)                 |

## Supported Diffusion Modles

| Model                                                                             | #Resp Format  | Checkpoint link                                                                                             |
| :-------------------------------------------------------------------------------- | :------------ | :---------------------------------------------------------------------------------------------------------- |
| [stable-diffusion-xl-base-1.0](https://github.com/Stability-AI/generative-models) | b64_json, url | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| [stable-diffusion-xl-base-0.9](https://github.com/Stability-AI/generative-models) | b64_json, url | [stabilityai/stable-diffusion-xl-base-0.9](https://huggingface.co/stabilityai/stable-diffusion-xl-base-0.9) |


## Supported Audio Models
| Model | #Params | Checkpoint link |
|:------|:--------|:---------------|
| [whisper-1](https://github.com/openai/whisper) | 1550 | alias for [whisper-large-v2](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt) |
| [whisper-large-v2](https://github.com/openai/whisper) | 1550 M | [large-v2](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt) |
| [whisper-medium](https://github.com/openai/whisper) | 769 M |  [medium](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt) |
| [whisper-small](https://github.com/openai/whisper) | 244 M |  [small](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt) |
| [whisper-base](https://github.com/openai/whisper) | 74 M | [base](https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt) |
| [whisper-tiny](https://github.com/openai/whisper) | 39 M | [tiny](https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt) |


## Example Code

### Stream Chat

```python
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

for chunk in openai.ChatCompletion.create(
    model="Baichuan-13B-Chat",
    messages=[{"role": "user", "content": "Which moutain is the second highest one in the world?"}],
    stream=True
):
    if hasattr(chunk.choices[0].delta, "content"):
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Chat

```python
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

resp = openai.ChatCompletion.create(
    model="Baichuan-13B-Chat",
    messages = [{ "role":"user", "content": "Which moutain is the second highest one in the world?" }]
)
print(resp.choices[0].message.content)
```

### Create Embeddings
```python
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

embeddings = openai.Embedding.create(
  model="gte-large",
  input="The food was delicious and the waiter..."
)

print(embeddings)
```

### List LLM Models

```python
import os
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

openai.Model.list()
```

### Create Image

```python
import os
import openai
from base64 import b64decode
from IPython.display import Image

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

response = openai.Image.create(
  prompt="An astronaut riding a green horse",
  n=1,
  size="1024x1024",
  response_format='b64_json'
)

b64_json = response['data'][0]['b64_json']
image = b64decode(b64_json)
Image(image)
```

### Create Transcription

```python
# Cell 1: set openai
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "None"

# Cell 2: create a recorder in notebook
# ===================================================
# sudo apt install ffmpeg
# pip install torchaudio ipywebrtc notebook
# jupyter nbextension enable --py widgetsnbextension

from IPython.display import Audio
from ipywebrtc import AudioRecorder, CameraStream

camera = CameraStream(constraints={'audio': True,'video':False})
recorder = AudioRecorder(stream=camera)
recorder

# Cell 3: transcribe
import os
import openai

temp_file = '/tmp/recording.webm'
with open(temp_file, 'wb') as f:
    f.write(recorder.audio.value)
audio_file = open(temp_file, "rb")

transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)
```

## Acknowledgement

项目参考了很多大佬的代码，例如 @xusenlinzy 大佬的[api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm/), @hiyouga 大佬的[LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning) 等，表示感谢。
