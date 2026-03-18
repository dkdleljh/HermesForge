from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_evidence_service
from app.schemas.evidence import EvidenceCreate, EvidenceRead
from app.services.evidence_service import EvidenceService

router = APIRouter(prefix="/evidence", tags=["evidence"])


@router.post("", response_model=EvidenceRead)
def create_evidence(payload: EvidenceCreate, service: EvidenceService = Depends(get_evidence_service)):
    return service.create(payload)


@router.get("", response_model=List[EvidenceRead])
def list_evidence(service: EvidenceService = Depends(get_evidence_service)):
    return service.list_all()
