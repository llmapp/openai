# coding=utf-8

import time

from fastapi import File
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional, Union


Role = Literal["user", "assistant", "system", "function"]


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"
    root: Optional[str] = None
    parent: Optional[str] = None
    permission: Optional[list] = []


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


class ChatMessage(BaseModel):
    role: Role
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Role] = None
    content: Optional[str] = None


class ChatFunction(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: dict


class CompletionRequest(BaseModel):
    model: str
    prompt: Union[str, List[str]]
    suffix: Optional[str] = None
    temperature: Optional[float] = 0.7
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    stream: Optional[bool] = False
    top_p: Optional[float] = 1.0
    logprobs: Optional[int] = None
    echo: Optional[bool] = False
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    user: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = 1
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

    functions: Optional[List[ChatFunction]] = None
    function_call: Optional[str] = None
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = 0
    frequnecy_penalty: Optional[float] = 0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]] = None


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0
    first_tokens: Optional[Any] = None


class ChatCompletionResponse(BaseModel):
    id: Optional[str] = None
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    usage: Optional[ChatCompletionResponseUsage] = None


class ChatCompletionStreamResponse(BaseModel):
    id: Optional[str] = "chatcmpl-default"
    model: str
    object: Literal["chat.completion.chunk"]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    choices: List[ChatCompletionResponseStreamChoice]


class EmbeddingsRequest(BaseModel):
    model: Optional[str] = None
    engine: Optional[str] = None
    input: Union[str, List[Any]]
    user: Optional[str] = None


class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: List[Dict[str, Any]]
    model: str
    usage: Optional[ChatCompletionResponseUsage] = None


class CreateImageRequest(BaseModel):
    prompt: str
    n: Optional[int] = 1
    size: Optional[Literal["256x256", "512x512", "1024x1024"]] = '1024x1024'
    response_format: Optional[Literal["url", "b64_json"]] = "url"
    user: Optional[str] = None


class _CreateImageResponseDataItem(BaseModel):
    url: Optional[str]
    b64_json: Optional[str]


class CreateImageResponse(BaseModel):
    created: int = Field(default_factory=lambda: int(time.time()))
    data: List[_CreateImageResponseDataItem]


# class AudioRequest(BaseModel):
#     file: bytes
#     model: str
#     prompt: Optional[str] = None
#     response_format: Optional[Literal["json", "text", "srt", "verbose_json", "vtt"]] = "json"
#     temperature: Optional[float] = 1.0
#     language: Optional[str]


class AudioResponse(BaseModel):
    text: str
