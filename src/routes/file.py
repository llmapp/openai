import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, UploadFile, Form
from uuid import uuid4

from ..type import DeleteFileResponse, ListFilesResponse, UploadFileResponse

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/openai.mini/files")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


file_router = APIRouter(prefix="/files")


# FIXME: Add authentication and upload file into user's folder and limit the folder capacity


@file_router.post("", response_model=UploadFileResponse)
async def upload_file(file: UploadFile, purpose: str = Form(...)):
    id = "file-" + str(uuid4()).replace("-", "")
    purpose = purpose.replace("_", "-")
    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, f"{id}_{purpose}_{filename}")
    with open(path, "wb") as f:
        f.write(file.file.read())

    return UploadFileResponse(id=id, bytes=file.size, filename=filename, purpose=purpose)


@file_router.get("/{id}", response_model=UploadFileResponse)
async def get_file_info(id: str):
    file = _find_file(id)
    if file:
        id = file.split("_")[0]
        purpose = file.split("_")[1]
        filename = "_".join(file.split("_")[2:])
        path = os.path.join(UPLOAD_FOLDER, file)
        bytes = os.path.getsize(path)
        created_at = os.path.getctime(path)
        return UploadFileResponse(id=id, bytes=bytes, filename=filename, purpose=purpose, created_at=created_at)
    else:
        raise HTTPException(status_code=404, detail=f"File {id} not found!")


@file_router.get("/{id}/content")
async def get_file_content(id: str):
    file = _find_file(id)
    if file:
        # get file content
        path = os.path.join(UPLOAD_FOLDER, file)
        with open(path, "rb") as f:
            content = f.read()
            return content
    else:
        raise HTTPException(status_code=404, detail=f"File {id} not found!")


@file_router.get("", response_model=ListFilesResponse)
async def list_files():
    data = []
    for file in os.listdir(UPLOAD_FOLDER):
        id = file.split("_")[0]
        purpose = file.split("_")[1]
        filename = "_".join(file.split("_")[2:])
        path = os.path.join(UPLOAD_FOLDER, file)
        bytes = os.path.getsize(path)
        created_at = os.path.getctime(path)
        item = UploadFileResponse(id=id, bytes=bytes, filename=filename, purpose=purpose, created_at=created_at)
        data.append(item)
    return ListFilesResponse(data=data)


@file_router.delete("/{id}", response_model=DeleteFileResponse)
async def delete_file(id: str):
    deleted = False
    filename = _find_file(id)
    path = os.path.join(UPLOAD_FOLDER, filename)
    if path:
        os.remove(path)
        deleted = True

    return DeleteFileResponse(id=id, deleted=deleted)


def _find_file(id: str):
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        if file.startswith(id):
            return file
    return None
