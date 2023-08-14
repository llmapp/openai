
from fastapi import APIRouter, HTTPException

from ..finetune import FineTuneRepo, FineTuneWorker
from ..type import CreateFineTuneRequest, FineTune, ListFineTuneEventsResponse, ListFineTunesResponse


fine_tune_router = APIRouter(prefix="/fine-tunes")


@fine_tune_router.post("", response_model=FineTune)
async def create_fine_tune(request: CreateFineTuneRequest):
    fine_tune = FineTuneWorker.train(request)
    return fine_tune


@fine_tune_router.get("", response_model=ListFineTunesResponse)
async def list_fine_tunes():
    return ListFineTunesResponse(data=FineTuneRepo.getAll())


@fine_tune_router.get("/{fine_tune_id}", response_model=FineTune)
async def retrieve_fine_tune(fine_tune_id: str):
    fine_tune = FineTuneRepo.get(fine_tune_id)
    if fine_tune:
        return fine_tune
    else:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")


@fine_tune_router.post("/{fine_tune_id}/cancel", response_model=FineTune)
async def cancel_fine_tune(fine_tune_id: str):
    if FineTuneRepo.get(fine_tune_id) is None:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")

    try:
        return FineTuneWorker.cancel(fine_tune_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")


@fine_tune_router.get("/{fine_tune_id}/events", response_model=ListFineTuneEventsResponse)
async def list_fine_tune_events(fine_tune_id: str):
    fine_tune = await retrieve_fine_tune(fine_tune_id)
    return ListFineTuneEventsResponse(data=fine_tune.events)