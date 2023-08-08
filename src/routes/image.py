import base64
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request
from io import BytesIO
from uuid import uuid4

from ..models import get_model
from ..models.image import ImageModel
from ..utils.constants import DEFAULT_IMAGE_FOLDER
from ..utils.request import raise_if_invalid_model

from ..type import CreateImageRequest, CreateImageResponse

load_dotenv()
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", DEFAULT_IMAGE_FOLDER)
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

image_router = APIRouter(prefix="/images")


DEFAULT_IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
@image_router.post("/generations", response_model=CreateImageResponse)
async def create_image(request: CreateImageRequest, req: Request):
    model = get_model(DEFAULT_IMAGE_MODEL)
    raise_if_invalid_model(model, ImageModel)

    width, height = request.size.split("x")
    width, height = int(width), int(height)
    prompt = [request.prompt] * request.n
    args = {"prompt": prompt,
            "height": 1024 if height == width else height,
            "width": 1024 if height == width else width}

    images = model.pipeline(**args).images
    data = []

    for image in images:
        if width == height:
            from PIL import Image
            image = image.resize((width, height), Image.ANTIALIAS)

        if request.response_format == "b64_json":
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            b64_json = base64.b64encode(buffered.getvalue())
            data.append({"b64_json": b64_json})
        elif request.response_format == "url":
            filename = "image-" + str(uuid4()).replace("-", "") + ".jpg"
            image_path = os.path.join(IMAGE_FOLDER, filename)
            image.save(image_path, format="JPEG")
            url = 'http://' + req.headers['host'] + os.path.join("/images", filename)
            data.append({"url": url})

    response = CreateImageResponse(data=data)
    return response
