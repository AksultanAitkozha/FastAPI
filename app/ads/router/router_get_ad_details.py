from fastapi import Depends, HTTPException, status
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class AdDetail(AppModel):
    _id: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str


@router.get("/shanyraks/{id}", response_model=AdDetail)
def get_ad_details(
    id: str,
    svc: Service = Depends(get_service),
) -> dict:
    ad = svc.repository.get_ad_by_id(id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found.",
        )

    return AdDetail(**ad)
