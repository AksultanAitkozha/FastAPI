from fastapi import Depends, UploadFile, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from typing import List

from ..service import Service, get_service
from . import router

'''
@router.post("/shanyraks/{shanyrak_id:str}/media")
def upload_file(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_file(file.file, file.filename)

    return {"msg": url}
'''


@router.post("/{shanyrak_id:str}/media")
def upload_files(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    if result is not None:
        svc.repository.upload_urls(shanyrak_id, jwt_data.user_id, result)
        return Response(status_code=200)
    return Response(status_code=404)
