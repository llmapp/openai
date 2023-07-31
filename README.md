# LLM as OpenAI

This repo implements OpenAI style APIs for large language models. With this repo, you can chat with LLMs using the [`openai` libraries](https://platform.openai.com/docs/api-reference)

## Development

### Install dependencies
 - `make install`

Start development server with the following command:
 - `cp .env.example .env`, and modify the `.env` file on your need
 - `make run`

Notice: the models can be loadded on startup or on the fly.

## Supported Audio Models
| Model | #Params | Checkpoint link |
|:------|:--------|:---------------|
| [whisper-large-v2](https://github.com/openai/whisper) | 1550 M | [openai/whisper-large-v2](https://huggingface.co/openai/whisper-large-v2) |
| [whisper-medium](https://github.com/openai/whisper) | 769 M |  [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) |
| [whisper-small](https://github.com/openai/whisper) | 244 M |  [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| [whisper-base](https://github.com/openai/whisper) | 74 M | [openai/whisper-base](https://huggingface.co/openai/whisper-base) |
| [whisper-tiny](https://github.com/openai/whisper) | 39 M | [openai/whisper-tiny](https://huggingface.co/openai/whisper-tiny) |

## Supported Diffusion Modles

| Model | #Resp Format| Checkpoint link |
|:------|:--------|:---------------|
| [stable-diffusion-xl-base-1.0](https://github.com/Stability-AI/generative-models) |  b64_json |                        [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| [stable-diffusion-xl-base-0.9](https://github.com/Stability-AI/generative-models) |  b64_json |                        [stabilityai/stable-diffusion-xl-base-0.9](https://huggingface.co/stabilityai/stable-diffusion-xl-base-0.9) |
## Supported Language Models

| Model | #Params | Checkpoint link |
|:------|:--------|:---------------|
| [FreeWilly2](https://stability.ai/blog/freewilly-large-instruction-fine-tuned-models) |  70B  |                        [stabilityai/FreeWilly2](https://huggingface.co/stabilityai/FreeWilly2) |
| [Llama-2-13b-chat-hf](https://github.com/facebookresearch/llama) |  13B  |                        [meta-llama/Llama-2-13b-chat-hf](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf) |
| [Llama-2-7b-chat-hf](https://github.com/facebookresearch/llama) |  7B  |                        [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf) |
|[Baichuan-13B-Chat](https://github.com/baichuan-inc/Baichuan-13B) | 13B | [baichuan-inc/Baichuan-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat)|
| [chatglm2-6b](https://github.com/THUDM/ChatGLM2-6B) |  6B  |                        [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b) |
| [chatglm-6b](https://github.com/THUDM/ChatGLM-6B) |  6B  | [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b) |
| [internlm-chat-7b](https://github.com/InternLM/InternLM)  |   7B    | [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b) |

## Example Code

### Create Image
``` python
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

### List LLM Models
``` python
import os
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

openai.Model.list()
```

### Normal Chat
``` python
import openai

openai.api_base = "http://localhost:8000/api/v1"
openai.api_key = "none"

resp = openai.ChatCompletion.create(
    model="Baichuan-13B-Chat",
    messages = [{ "role":"user", "content": "Which moutain is the second highest one in the world?" }]
)
print(resp.choices[0].message.content)
```

### Stream Chat

``` python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "none"

for chunk in openai.ChatCompletion.create(
    model="Baichuan-13B-Chat",
    messages=[{"role": "user", "content": "Which moutain is the second highest one in the world?"}],
    stream=True
):
    if hasattr(chunk.choices[0].delta, "content"):
        print(chunk.choices[0].delta.content, end="", flush=True)
```