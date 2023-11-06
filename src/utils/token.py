from pydantic import BaseModel
from typing import List
import tiktoken
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

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
