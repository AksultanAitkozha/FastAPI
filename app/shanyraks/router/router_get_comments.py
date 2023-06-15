from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class CommentResponse(AppModel):
    _id: str
    content: str
    created_at: str
    author_id: str


@router.get(
    "/{shanyrak_id:str}/comments", response_model=dict[str, list[CommentResponse]]
)
def get_comments(
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    ad = svc.repository.get_ad_by_id(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found or has no comments")

    comments = svc.repository.get_comments(ad_id)

    return comments
