from fastapi import Depends
from typing import Any, Optional
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from pydantic import Field
from . import router


class Location(AppModel):
    latitude: Optional[float]
    longitude: Optional[float]


class HouseAd(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    location: Location


class AdResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", response_model=AdResponse)
def create_ad(
    input: HouseAd,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> dict[str, str]:
    # Get coordinates for address
    result = svc.here_service.get_coordinates(input.address)
    lat, lng = result['lat'], result['lng']

    # Set latitude and longitude
    input.location = Location(latitude=lat, longitude=lng)

    # Extract user_id from jwt_data and create new ad
    housead_id = svc.repository.create_new_ad(jwt_data.user_id, input.dict())

    return AdResponse(id=housead_id)
