from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.post("/users/favorites/shanyraks/{ad_id:str}")
def add_ad_to_favorites(
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    # Extract user_id from jwt_data
    user_id = jwt_data.user_id

    # Call the service/repository method to add the ad to the user's favorites
    success = svc.repository.add_to_favorites(user_id, ad_id)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to add ad to favorites")

    return {"status": "Ad added to favorites"}
