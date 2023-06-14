from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from . import router


class UpdateAd(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def update_ad(
    ad_id: str,
    input: UpdateAd,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    res_update = svc.repository.update_ad(ad_id, jwt_data.user_id, input.dict())
    if res_update.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
