from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{shanyrak_id:str}/comments/{comment_id:str}")
def update_comment(
    ad_id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    update_result = svc.repository.update_comment(
        ad_id, comment_id, user_id, input.content
    )
    if update_result.modified_count:
        return {"message": "Comment updated successfully"}
    raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
