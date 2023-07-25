from pydantic import BaseModel
from typing import List

from ..type import ChatMessage


DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
"""


class TokenFormatConfig(BaseModel):
    SYSTEM_PROMPT: str = DEFAULT_SYSTEM_PROMPT
    B_SYS: str = "<<SYS>>\n"
    E_SYS: str = "\n<</SYS>>\n\n"
    B_INST: str = "[INST]"
    E_INST: str = "[/INST]"
    B_AI: str = ""
    E_AI: str = ""


def format_tokens(dialog, tokenizer, config):
    if dialog[0].role != "system":
        dialog = [ChatMessage(role="system", content=config.SYSTEM_PROMPT)] + dialog
    dialog = [ChatMessage(role=dialog[1].role, content=config.B_SYS
                          + dialog[0].content
                          + config.E_SYS
                          + dialog[1].content)] + dialog[2:]
    assert all([msg.role == "user" for msg in dialog[::2]]) and all(
        [msg.role == "assistant" for msg in dialog[1::2]]
    ), (
        "model only supports 'system','user' and 'assistant' roles, "
        "starting with user and alternating (u/a/u/a/u...)"
    )
    dialog_tokens: List[int] = sum(
        [tokenizer.encode(compose_qa(prompt, answer, config)) for prompt, answer in zip(dialog[::2], dialog[1::2])],
        [],
    )
    assert (
        dialog[-1].role == "user"
    ), f"Last message must be from user, got {dialog[-1].role}"
    dialog_tokens += tokenizer.encode(
        f"{config.B_INST} {(dialog[-1].content).strip()} {config.E_INST}",
    )

    return dialog_tokens


def compose_qa(prompt, answer, config):
    return f"{config.B_INST}{(prompt.content).strip()}{config.E_INST} {config.B_AI}{(answer.content).strip()}{config.E_AI}"
