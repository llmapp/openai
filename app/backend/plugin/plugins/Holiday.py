import datetime
from typing import Any, List

from ..type import Argument, Plugin



class Holiday(Plugin):
    name = "Holiday"
    name_for_human = "HolidayQuery"
    description = "可以用来查询各个国家公开的法定节假日时间。"
    arguments: List[Argument] = [
        Argument(name="countryCode", type="string", description="国家的ISO 3166-1二位字母代码，例如 CN 表示中国，GB 表示英国", required=False),
        Argument(name="year", type="int", description="哪一年的节日", required=False),
    ]

    def run(self, args: str) -> Any:
        params = super().run(args)
        countryCode = params["countryCode"] if "countryCode" in params else "CN"
        year = params["year"] if "year" in params else datetime.date.today().year

        url = f"https://date.nager.at/Api/v2/PublicHolidays/{year}/{countryCode}"
        import requests
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            return "查询失败"
        
        if response.status_code != 200:
            return "查询失败"
        return response.json()
