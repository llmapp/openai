# coding=utf-8

import time

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


class FunctionCallResponse(BaseModel):
    name: Optional[str]
    arguments: Optional[str]


class ChatMessage(BaseModel):
    role: Role
    content: str = None
    name: Optional[str] = None
    function_call: Optional[FunctionCallResponse] = None


class DeltaMessage(BaseModel):
    role: Optional[Role] = None
    content: Optional[str] = None
    function_call: Optional[FunctionCallResponse] = None


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
    function_call: Union[str, Dict[str, str]] = "auto"
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = 0
    frequnecy_penalty: Optional[float] = 0
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length", "function_call"] = None


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length", "function_call"]] = None


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0
    first_tokens: Optional[Any] = None


class ChatCompletionResponse(BaseModel):
    id: Optional[str] = None
    object: Literal["chat.completion", "chat.completion.chunk"]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    usage: Optional[UsageInfo] = None


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
    usage: Optional[UsageInfo] = None


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


class AudioResponse(BaseModel):
    text: str


class UploadFileResponse(BaseModel):
    id: str
    object: str = "file"
    bytes: int
    created_at: int = Field(default_factory=lambda: int(time.time()))
    filename: str
    purpose: Literal['fine-tune', 'search']  # | str


class ListFilesResponse(BaseModel):
    data: List[UploadFileResponse]
    object: str = "list"


class DeleteFileResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool


class CreateFineTuneRequest(BaseModel):
    training_file: str
    validation_file: Optional[str]
    model: Literal["ada", "babbage", "curie", "davinci"] = "curie"  # | str = "curie"
    n_epochs: Optional[int] = 4
    batch_size: Optional[int] = None
    learning_rate_multiplier: Optional[float] = None
    prompt_loss_weight: Optional[float] = 0.01
    compute_classification_metrics: Optional[bool] = False
    classification_n_classes: Optional[int] = None
    classification_positive_class: Optional[str] = None
    classification_betas: Optional[List[float]] = None
    suffix: Optional[str] = None


class CreateFineTuneResponse(BaseModel):
    id: str
    object: str = "fine-tune"
    model: str
    created_at: int = Field(default_factory=lambda: int(time.time()))
    updated_at: int = Field(default_factory=lambda: int(time.time()))
    status: Literal["pending", "running", "completed", "failed"]
    # TODO: more ...
