import openai
from typing import List

from ..type import Argument, Plugin

# load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY", "none")
# if os.getenv("OPENAI_API_BASE", None) is not None:
#     openai.api_base = os.getenv("OPENAI_API_BASE")

openai.api_key = "none"
openai.api_base = "http://localhost:8000/api/v1"

class SDXL(Plugin):
    name = "gen_image_with_sdxl"
    name_for_human = "SDXL图片生成"
    description = "根据用户输入的prompt内容生成图片"
    arguments: List[Argument] = [
        Argument(name="prompt", type="string", description="The prompt for generating image.", required=True),
        Argument(name="size", type="string", description="The size of the images to be generated.", required=False),
        Argument(name="count", type="number", description="The count of how many images to be generated.", required=False)
    ]

    def run(self, args: str) -> str or None:
        params = super().run(args)
        if params is None or "prompt" not in params:
            return None

        prompt = params["prompt"]
        size = params["size"] if "size" in params and params["size"] in [
            "1024x1024", "512x512", "256x256"] else "1024x1024"
        count = params["count"] if "count" in params and type(params["count"]) == int else 1

        return openai.Image.create(prompt=prompt, n=count, size=size)
