from pydantic import BaseModel
from uuid import uuid4

from ..type import CreateFineTuneRequest, File, FineTune, FineTuneEvent, FineTuneHyperparams


FINE_TUNES_REPO = {}

WORKERS = {}

class FineTuneWorker(BaseModel):
    training_id: str
    fine_tune: FineTune

    @staticmethod
    def train(params: CreateFineTuneRequest):
        id = "ft-" + str(uuid4()).replace("-", "")
        # TODO: do something
        fine_tune = FineTune(
            id=id,
            model="curie",
            events=[
                FineTuneEvent(
                    object="fine-tune-event",
                    level="info",
                    message="Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
                )
            ],
            hyperparams=FineTuneHyperparams(
                batch_size=4,
                learning_rate_multiplier=0.1,
                n_epochs=4,
                prompt_loss_weight=0.1,
            ),
            organization_id="org-...",
            result_files=[],
            status="pending",
            validation_files=[],
            training_files=[
                File(
                    id="file-XGinujblHPwGLSztz8cPS8XY",
                    object="file",
                    bytes=1547276,
                    created_at=1610062281,
                    filename="my-data-train.jsonl",
                    purpose="fine-tune-train"
                ) 
            ]
        )
        
        worker = FineTuneWorker(training_id='1', fine_tune=fine_tune)

        WORKERS[fine_tune.id] = worker
        FINE_TUNES_REPO[fine_tune.id] = fine_tune

        return fine_tune


    @staticmethod
    def cancel(id: str):
        worker = WORKERS.pop(id)
        if not worker:
            raise Exception(f"Worker {id} not found!")

        # TODO: do something
        fine_tune = worker.fine_tune
        fine_tune.status = "cancelled"

        return fine_tune