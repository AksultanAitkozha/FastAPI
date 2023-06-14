from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from app.utils import AppModel
from typing import List
from ..service import Service, get_service

from . import router


class MediaDelete(AppModel):
    media: List[str]


@router.delete("/{shanyrak_id:str}/media")
def delete_media(
    ad_id: str,
    media: MediaDelete,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_media(ad_id, jwt_data.user_id, media.media)
    if delete_result.modified_count:
        return Response(status_code=200)
    return Response(status_code=404)
