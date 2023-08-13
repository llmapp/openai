
from fastapi import APIRouter, HTTPException

from ..finetune import FineTuneWorker, FINE_TUNES_REPO
from ..type import CreateFineTuneRequest, FineTune, ListFineTuneEventsResponse, ListFineTunesResponse


fine_tune_router = APIRouter(prefix="/fine-tunes")

@fine_tune_router.post("", response_model=FineTune)
async def create_fine_tune(request: CreateFineTuneRequest):
    fine_tune = FineTuneWorker.train(request)
    FINE_TUNES_REPO[fine_tune.id] = fine_tune
    return fine_tune

@fine_tune_router.get("", response_model=ListFineTunesResponse)
async def list_fine_tunes():
    data = list(FINE_TUNES_REPO.values())
    return ListFineTunesResponse(data=data)

@fine_tune_router.get("/{fine_tune_id}", response_model=FineTune)
async def retrieve_fine_tune(fine_tune_id: str):
    fine_tune = FINE_TUNES_REPO.get(fine_tune_id)
    if fine_tune:
        return fine_tune
    else:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")

@fine_tune_router.post("/{fine_tune_id}/cancel", response_model=FineTune)
async def cancel_fine_tune(fine_tune_id: str):
    if fine_tune_id not in FINE_TUNES_REPO:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")

    try:
        return FineTuneWorker.cancel(fine_tune_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Fine-tune {fine_tune_id} not found!")

@fine_tune_router.get("/{fine_tune_id}/events", response_model=ListFineTuneEventsResponse)
async def list_fine_tune_events(fine_tune_id: str):
    fine_tune = await retrieve_fine_tune(fine_tune_id)
    return ListFineTuneEventsResponse(data=fine_tune.events)