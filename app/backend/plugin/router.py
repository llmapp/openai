
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, List

from .plugins import get_plugins, get_plugin
from .type import Plugin


router = APIRouter(prefix="/plugins", tags=["Plugin"])


@router.get("", response_model=List[Plugin])
async def list_plugins():
    return get_plugins()


class ArgsRequest(BaseModel):
    name: str
    args: str


@router.post("/run", response_model=Any)
async def run_plugin(request: ArgsRequest):
    plugin_name, args = request.name, request.args
    plugin = get_plugin(plugin_name)
    if plugin is None:
        raise HTTPException(status_code=404, detail=f"Plugin {plugin_name} not found!")

    result = plugin.run(args)
    if result is None:
        raise HTTPException(status_code=400, detail=f"Plugin {plugin_name} failed to run!")

    return result
