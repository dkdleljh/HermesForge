from typing import List
from uuid import uuid4

from app.domain.entities import LambdaPatch
from app.repositories.base import PatchRepository
from app.schemas.patch import LambdaPatchCreate


class PatchService:
    def __init__(self, repo: PatchRepository):
        self.repo = repo

    def create(self, payload: LambdaPatchCreate) -> LambdaPatch:
        patch = LambdaPatch(
            id=f"lp-{uuid4().hex[:12]}",
            conditions=payload.conditions,
            outcome=payload.outcome,
            probability_mass=payload.probability_mass,
            confidence=payload.confidence,
            constraint_proof=payload.constraint_proof,
            witness_refs=payload.witness_refs,
            anchor_weight=payload.anchor_weight,
            labels=payload.labels,
        )
        return self.repo.create(patch)

    def list_all(self) -> List[LambdaPatch]:
        return self.repo.list_all()

    def get(self, patch_id: str) -> LambdaPatch | None:
        return self.repo.get(patch_id)
