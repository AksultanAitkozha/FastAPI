from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class UpdateUserInfo(AppModel):
    phone: str
    name: str
    city: str


@router.patch("/auth/users/me")
def update_user_info(
    input: UpdateUserInfo,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    svc.repository.update_user(user_id, input.dict())
    return {"detail": "info updated"}