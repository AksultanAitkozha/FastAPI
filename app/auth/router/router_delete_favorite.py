from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/users/favorites/shanyraks/{ad_id:str}")
def remove_from_favorites(
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    success = svc.repository.remove_from_favorites(jwt_data.user_id, ad_id)
    if not success:
        raise HTTPException(status_code=400, detail="Ad not found in favorites")
    return {"status": "success"}
