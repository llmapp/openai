# coding=utf-8

import time

from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union


Role = Literal["user", "assistant", "system", "function"]


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"
    root: Optional[str] = None
    parent: Optional[str] = None
    permission: Optional[list] = None


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


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = 1
    stream: Optional[bool] = False

    functions: Optional[List[ChatFunction]] = None
    function_call: Optional[str] = None
    n: Optional[int] = 1
    stop: Optional[List[str]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0
    frequnecy_penalty: Optional[float] = 0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    usage: Optional[ChatCompletionResponseUsage] = None
