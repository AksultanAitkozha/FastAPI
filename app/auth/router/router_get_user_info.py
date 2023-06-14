from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from typing import Optional

from ..service import Service, get_service
from . import router


class GetUserInfoResponse(AppModel):
    _id: str
    email: str
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None


# Define a User model to represent the user's data.
class User(AppModel):
    _id: str
    email: str
    phone: str
    name: str
    city: str


@router.get("/users/me", response_model=User)
def get_user_info(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, Optional[str]]:
    user_id = jwt_data.user_id
    user = svc.repository.get_user_by_id(user_id)
    return user
