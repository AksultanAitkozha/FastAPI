from fastapi import APIRouter, Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from pydantic import BaseModel
from pydantic import Field
from . import router


class HouseAd(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class AdResponse(BaseModel):
    _id: str = Field(alias="_id")


@router.post("/", response_model=AdResponse, status_code=200)
def create_ad(
    ad: HouseAd,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> str:
    # Extract user_id from jwt_data
    user_id = jwt_data.user_id

    # Insert the ad into the database and get the id of the new ad
    ad_id = svc.repository.create_new_ad(user_id, ad.dict())

    # If the ad was created successfully, return its id
    if ad_id:
        return {"_id": ad_id}
    else:
        raise HTTPException(status_code=400, detail="Ad could not be created")
