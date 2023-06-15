from fastapi import Depends, Response
from app.utils import AppModel
from ..service import Service, get_service
from . import router
from typing import Any
from pydantic import Field
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class AdDetail(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    latitude: float  # new
    longitude: float  # new


@router.get("/{shanyrak_id:str}", response_model=AdDetail)
def get_ad_details(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    ad = svc.repository.get_ad_by_id(shanyrak_id)
    if ad is None:
        return Response(status_code=404)
    return AdDetail(**ad)
