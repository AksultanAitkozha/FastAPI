from typing import Optional
from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class User(AppModel):
    _id: str
    email: str
    phone: str
    name: str
    city: str
    avatar_url: Optional[str] = None


@router.get("/users/me", response_model=User)
def get_user_info(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, Optional[str]]:
    user_id = jwt_data.user_id
    user_dict = svc.repository.get_user_by_id(user_id)
    if "avatar_url" in user_dict:
        user_dict["avatar_url"] = user_dict["avatar_url"]
    return user_dict
