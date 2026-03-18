from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_patch_service
from app.schemas.patch import LambdaPatchCreate, LambdaPatchRead
from app.services.patch_service import PatchService

router = APIRouter(prefix="/patches", tags=["patches"])


@router.post("", response_model=LambdaPatchRead)
def create_patch(payload: LambdaPatchCreate, service: PatchService = Depends(get_patch_service)):
    return service.create(payload)


@router.get("", response_model=List[LambdaPatchRead])
def list_patches(service: PatchService = Depends(get_patch_service)):
    return service.list_all()
