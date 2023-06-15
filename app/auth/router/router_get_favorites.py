from typing import List
from pydantic import Field
from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class Ad(AppModel):
    _id: str = Field(alias="ad_id")
    address: str


class GetFavoritesResponse(AppModel):
    shanyraks: List[Ad]


@router.get("/users/favorites/shanyraks", response_model=GetFavoritesResponse)
def get_user_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, List[dict]]:
    favorites = svc.repository.get_favorites(jwt_data.user_id)
    return {"shanyraks": favorites}
