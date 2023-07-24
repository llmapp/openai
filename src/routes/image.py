import base64

from fastapi import APIRouter
from io import BytesIO

from ..diffusers import get_model
from ..utils.logger import get_logger

from ..type import CreateImageRequest, CreateImageResponse


image_router = APIRouter(prefix="/images")

logger = get_logger(__name__)


@image_router.post("/generations", response_model=CreateImageResponse)
async def create_image(request: CreateImageRequest):
    model = get_model()

    width, height = request.size.split("x")
    prompt = [request.prompt] * request.n
    args = {"prompt": prompt, "height": int(height), "width": int(width)}

    images = model.pipe(**args).images
    if request.response_format == "b64_json":
        data = []
        for image in images:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            b64_json = base64.b64encode(buffered.getvalue())
            data.append({"b64_json": b64_json})
    else:
        raise NotImplementedError()
        # data = [{"url": image.url} for image in images]

    response = CreateImageResponse(data=data)
    return response
