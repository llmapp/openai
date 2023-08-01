
from fastapi import APIRouter
from ..type import CreateFineTuneRequest, CreateFineTuneResponse


fine_tune_router = APIRouter(prefix="/fine-tunes")


@fine_tune_router.post("")  # , response_class=CreateFineTuneResponse)
async def create_fine_tune(request: CreateFineTuneRequest):
    print(request)
    return None
