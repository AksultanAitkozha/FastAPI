from fastapi import Depends, UploadFile, File, Response
from app.auth.adapters.jwt_service import JWTData
from app.utils import AppModel
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class UploadAvatarResponse(AppModel):
    avatar_url: str


@router.post("/users/avatar", response_model=UploadAvatarResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Name of the file
    file.file: BytesIO - Content of the file
    """
    url = svc.s3_service.upload_file(file.file, file.filename)
    if url:
        svc.repository.upload_avatar(jwt_data.user_id, url)
        return {"avatar_url": url}
    else:
        return Response(status_code=404)
