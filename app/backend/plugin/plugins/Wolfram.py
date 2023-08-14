from typing import Any, List
from dotenv import load_dotenv
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from ..type import Argument, Plugin

load_dotenv()

wolfram = WolframAlphaAPIWrapper()


class Wolfram(Plugin):
    name = "wolfram"
    name_for_human = "Wolfram Alpha"
    description = "可以用来计算数学题目、方程求解等数学方面的运算，也可以用来解答一些具有时效性的问题，例如，当前的金价是多少、美国的首都是哪里等问题。"
    arguments: List[Argument] = [
        Argument(name="query", type="string", description="要计算或着求解的内容，或者是需要查询的内容", required=True)
    ]

    def run(self, args: str) -> Any:
        params = super().run(args)
        query = params["query"] if "query" in params else None
        if query is None:
            return None

        result = wolfram.run(query)
        parts = result.split("\nAnswer: ")
        return parts[-1].strip()
