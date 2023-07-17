# LLM as OpenAI

This repos is an implementation of rest APIs for accessing large language models like OpenAI API.

## Development

### Install dependencies
 - `make install`

Start development server with the following command:
 - `cp .env.example .env`, and modify the `.env` file on your need
 - `make run`

Notice: the models can be loadded on startup or on the fly.

## Supported Models

| Model | #Params | Checkpoint link |
|:------|:--------|:---------------|
|[Baichuan-13b-chat](https://github.com/baichuan-inc/Baichuan-13B) | 13B | [baichuan-inc/Baichuan-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat)|
| [internlm-chat-7b](https://github.com/InternLM/InternLM)  |   7B    | [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b) |
| [chatglm2-6b](https://github.com/THUDM/ChatGLM2-6B) |  6B  |                        [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b) |
| [chatglm-6b](https://github.com/THUDM/ChatGLM-6B) |  6B  | [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b) |

## Example Code

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