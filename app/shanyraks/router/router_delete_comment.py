from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id:str}/comments/{comment_id:str}")
def delete_comment(
    ad_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    delete_result = svc.repository.delete_comment(ad_id, comment_id, user_id)
    if delete_result.modified_count:
        return {"message": "Comment deleted successfully"}
    raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
