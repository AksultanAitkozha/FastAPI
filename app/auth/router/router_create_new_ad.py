from typing import Any
from pydantic import Field
from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


# Define a new Pydantic model for the house ad data
class HouseAd(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


# Define a model for the response
class HouseAdResponse(AppModel):
    _id: Any = Field(alias="_id")


@router.post("/shanyraks", response_model=HouseAdResponse)
def create_house_ad(
    ad: HouseAd,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, Any]:
    user_id = jwt_data.user_id
    ad_id = svc.repository.create_ad(user_id, ad.dict())
    return {"_id": ad_id}
