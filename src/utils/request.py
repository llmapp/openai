
from fastapi import HTTPException

def raise_if_invalid_model(model, type):
    if model is None or not isinstance(model, type):
        raise HTTPException(status_code=400, detail="Invalid request model")