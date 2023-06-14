from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from pydantic import Field
from app.utils import AppModel
from typing import Any, List

from ..service import Service, get_service

from . import router


class FileDetails(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    media: List[str]


@router.get("/{shanyrak_id:str}", response_model=FileDetails)
def get_file_details(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    ad = svc.repository.get_ad_by_id(shanyrak_id)
    if ad is None:
        return Response(status_code=404)
    return FileDetails(**ad)
