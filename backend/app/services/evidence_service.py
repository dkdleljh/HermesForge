from typing import List
from uuid import uuid4

from app.domain.entities import Evidence
from app.repositories.base import EvidenceRepository
from app.schemas.evidence import EvidenceCreate
from app.utils.hash_utils import stable_hash


class EvidenceService:
    def __init__(self, repo: EvidenceRepository):
        self.repo = repo

    def create(self, payload: EvidenceCreate) -> Evidence:
        evidence = Evidence(
            id=f"ev-{uuid4().hex[:12]}",
            source=payload.source,
            payload=payload.payload,
            trust_score=payload.trust_score,
            timestamp=payload.timestamp,
            hash=stable_hash({"source": payload.source, "payload": payload.payload, "timestamp": payload.timestamp}),
        )
        return self.repo.create(evidence)

    def list_all(self) -> List[Evidence]:
        return self.repo.list_all()
