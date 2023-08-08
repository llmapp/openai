
from typing import List

from .llama import LLaMA
from src.utils.token import TokenFormatConfig

_SYSTEM_PROMPT = "\
You are Free Willy, an AI that follows instructions extremely well. \
Help as much as you can. Remember, be safe, and don't do anything illegal."

_token_format_config = TokenFormatConfig(
    SYSTEM_PROMPT=_SYSTEM_PROMPT,
    B_SYS="### System:\n", E_SYS="\n\n",
    B_INST="### User:\n", E_INST="\n\n",
    B_AI="### Assistant:\n", E_AI="\n\n")


class FreeWilly2(LLaMA):
    def chat(self, messages: List[str], stream: bool = False, **kwargs):
        return super().chat(messages, stream, token_format_config=_token_format_config, **kwargs)