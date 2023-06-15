from fastapi import HTTPException
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/users/avatar")
def delete_avatar(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    # Extract the user_id from the JWT token
    user_id = jwt_data.user_id

    # Remove the avatar
    result = svc.repository.delete_avatar(user_id)
    if result is None:
        return Response(status_code=200, detail="Avatar deleted!")
    else:
        raise HTTPException(status_code=400, detail="Failed to delete avatar")
