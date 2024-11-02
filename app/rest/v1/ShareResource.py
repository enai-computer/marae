from fastapi import APIRouter, Depends
from typing import Annotated
from app.services.CheckTokenService import get_current_user
from app.rest.models.ShareModels import SharePayload, ShareResponse
from app.services.SharingService import SharingService
from uuid import UUID

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/{user_id}/share")
def share_fetch(user_id: UUID, share_id: str, sharing_service: Annotated[SharingService, Depends(SharingService)]) -> SharePayload:
    return sharing_service.fetch_shared_obj(user_id, share_id)

@router.post("/{user_id}/share")
def share_store(user_id: UUID, payload: SharePayload, sharing_service: Annotated[SharingService, Depends(SharingService)]) -> ShareResponse:
    key = sharing_service.store_shared_obj(user_id, payload)
    print(f"Share key: {key}")
    return ShareResponse(share_id=key)
