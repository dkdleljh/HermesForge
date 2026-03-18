from fastapi import APIRouter, Depends

from app.api.deps import get_policy_service
from app.schemas.policy import PolicyResponse
from app.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=PolicyResponse)
def get_policies(service: PolicyService = Depends(get_policy_service)):
    return service.get_policy()
