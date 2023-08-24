# coding=utf-8

import time

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional, Union


Role = Literal["user", "assistant", "system", "function"]


class FunctionCallResponse(BaseModel):
    name: Optional[str]
    arguments: Optional[str]


class ChatMessage(BaseModel):
    role: Optional[Role]
    content: Optional[str] = None
    function_call: Optional[FunctionCallResponse]


class ChatFunction(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: dict


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    functions: Optional[List[ChatFunction]] = None
    function_call: Union[str, Dict[str, str]] = "auto"
    stream: Optional[bool] = False

    temperature: Optional[float] = None
    top_p: Optional[float] = 1
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: ChatMessage
    finish_reason: Optional[Literal["stop", "length", "function_call"]] = None


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0
    first_tokens: Optional[Any] = None


class ChatCompletionResponse(BaseModel):
    id: Optional[str] = "chatcmpl-default"
    model: str
    object: Literal["chat.completion.chunk"]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    choices: List[ChatCompletionResponseStreamChoice]
    usage: Optional[UsageInfo] = None