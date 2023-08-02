# LLM as OpenAI

This repo implements OpenAI style APIs for large language models. With this repo, you can chat with LLMs using the [`openai` libraries](https://platform.openai.com/docs/api-reference)

## Development

### Install dependencies

- `make install`

Start development server with the following command:

- `cp .env.example .env`, and modify the `.env` file on your need
- `make run`

Notice: the models can be loadded on startup or on the fly.

## Status

| Services          | API                      | Status           | Description             |
| :-----------------| :------------------------| :----------------| :-----------------------|
| Authorization     |                          |                  |                         |
| Models            |                          |                  |                         |
|                   | List models              | Done             |                         |
|                   | Retrieve model           |                  |                         |
| Chat              |                          |                  | Support Multi. LLMs     |
|                   | Create chat completion   | Partial Done     | Response format         |
| Completions       |                          |                  |                         |
|                   | Create completion        |                  |                         |
| Images            |                          |                  |                         |
|                   | Create image             | Partial Done     |                         |
|                   | Create image edit        |                  |                         |
|                   | Create image variation   |                  |                         |
| Embeddings        |                          |                  |                         |
|                   | Create embeddings        |                  |                         |
| Audio             |                          |                  |                         |
|                   | Create transcription     | Done             |                         |
|                   | Create translation       | Done             |                         |
| Files             |                          |                  |                         |
|                   | List files               | Done             |                         |
|                   | Upload file              | Done             |                         |
|                   | Delete file              | Done             |                         |
|                   | Retrieve file            | Done             |                         |
|                   | Retrieve file content    | Done             |                         |
| Fine-tunes        |                          |                  |                         |
|                   | Create fine-tune         |                  |                         |
|                   | List fine-tunes          |                  |                         |
|                   | Retrieve fine-tune       |                  |                         |
|                   | Cancel fine-tune         |                  |                         |
|                   | List fine-tune events    |                  |                         |
|                   | Delete fine-tune model   |                  |                         |
| Moderations       |                          |                  |                         |
| Edits             |                          |                  |                         |

## Supported Language Models

| Model                                                                                 | #Params | Checkpoint link                                                                         |
| :------------------------------------------------------------------------------------ | :------ | :-------------------------------------------------------------------------------------- |
| [FreeWilly2](https://stability.ai/blog/freewilly-large-instruction-fine-tuned-models) | 70B     | [stabilityai/FreeWilly2](https://huggingface.co/stabilityai/FreeWilly2)                 |
| [Llama-2-13b-chat-hf](https://github.com/facebookresearch/llama)                      | 13B     | [meta-llama/Llama-2-13b-chat-hf](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf) |
| [Llama-2-7b-chat-hf](https://github.com/facebookresearch/llama)                       | 7B      | [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)   |
| [Baichuan-13B-Chat](https://github.com/baichuan-inc/Baichuan-13B)                     | 13B     | [baichuan-inc/Baichuan-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat) |
| [chatglm2-6b](https://github.com/THUDM/ChatGLM2-6B)                                   | 6B      | [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)                           |
| [chatglm-6b](https://github.com/THUDM/ChatGLM-6B)                                     | 6B      | [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)                             |
| [internlm-chat-7b](https://github.com/InternLM/InternLM)                              | 7B      | [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b)           |

## Supported Diffusion Modles

| Model                                                                             | #Resp Format | Checkpoint link                                                                                             |
| :-------------------------------------------------------------------------------- | :----------- | :---------------------------------------------------------------------------------------------------------- |
| [stable-diffusion-xl-base-1.0](https://github.com/Stability-AI/generative-models) | b64_json     | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| [stable-diffusion-xl-base-0.9](https://github.com/Stability-AI/generative-models) | b64_json     | [stabilityai/stable-diffusion-xl-base-0.9](https://huggingface.co/stabilityai/stable-diffusion-xl-base-0.9) |


## Supported Audio Models
| Model | #Params | Checkpoint link |
|:------|:--------|:---------------|
| [whisper-1](https://github.com/openai/whisper) | 1550 | alias for [whisper-large-v2](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt) |
| [whisper-large-v2](https://github.com/openai/whisper) | 1550 M | [large-v2](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt) |
| [whisper-medium](https://github.com/openai/whisper) | 769 M |  [medium](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt) |
| [whisper-small](https://github.com/openai/whisper) | 244 M |  [small](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt) |
| [whisper-base](https://github.com/openai/whisper) | 74 M | [base](https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt) |
| [whisper-tiny](https://github.com/openai/whisper) | 39 M | [tiny](https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt) |
       |

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

### Normal Chat

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
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "None"

audio_file = open("audio.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)
```
