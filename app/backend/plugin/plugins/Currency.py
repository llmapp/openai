from typing import Any, List

from ..type import Argument, Plugin


apiVersion = "1"

class Currency(Plugin):
    name = "Currency"
    name_for_human = "Currency"
    description = "可以用来进行汇率转换，例如人民币兑美元的汇率是多少。"
    arguments: List[Argument] = [
        Argument(name="from_code", type="string", description="汇率的ISO 4217 三位字母代码，例如 CNY 表示人民币，USD 表示美元", required=True),
        Argument(name="to_code", type="string", description="汇率的ISO 4217 三位字母代码，例如 CNY 表示人民币，USD 表示美元", required=True),
        Argument(name="date", type="string", description="哪天的汇率，要求为`YYYY-MM-DD`的日期格式，如果为空，则表示是查询最新的汇率", required=False),
    ]

    def run(self, args: str) -> Any:
        params = super().run(args)
        from_code = params["from_code"] if "from_code" in params else "CNY"
        to_code = params["to_code"] if "to_code" in params else "USD"
        date = params["date"] if "date" in params else "latest"
        pattern_str = r'^\d{4}-\d{2}-\d{2}$'
        import re
        date = date if re.match(pattern_str, date) is not None else "latest"
        # url = f"https://raw.githubusercontent.com/fawazahmed0/currency-api/{apiVersion}/{date}/currencies/{from_code.lower()}/{to_code.lower()}.json"
        url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@{apiVersion}/{date}/currencies/{from_code.lower()}/{to_code.lower()}.json"
        import requests
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            return "查询失败"
        
        if response.status_code != 200:
            return "查询失败"
        return response.json()
