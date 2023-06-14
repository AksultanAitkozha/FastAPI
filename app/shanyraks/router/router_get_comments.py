from fastapi import Depends
from typing import List, Any
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from pydantic import Field
from app.shanyraks.service import Service, get_service
from . import router


class CommentResponse(AppModel):
    _id: str
    author_id: str
    content: str
    created_at: str


@router.get("/{ad_id}/comments", response_model=List[CommentResponse])
def get_comments(
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> List[CommentResponse]:
    comments = svc.repository.get_comments(ad_id)
    return comments
