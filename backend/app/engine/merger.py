from typing import Dict, List

from app.domain.entities import LambdaPatch, Snapshot
from app.engine.interfaces import Merger

FORBIDDEN_CATEGORIES = {"harmful", "illegal", "factual_claim"}


class PolicyAwareMerger(Merger):
    """병합 시 forbidden category를 제거한다."""

    def merge(self, left: Snapshot, right: Snapshot, left_patches: List[LambdaPatch], right_patches: List[LambdaPatch]) -> List[LambdaPatch]:
        merged: Dict[str, LambdaPatch] = {}
        for patch in [*left_patches, *right_patches]:
            category = patch.outcome.get("category", "general")
            if category in FORBIDDEN_CATEGORIES:
                continue
            if patch.id not in merged:
                merged[patch.id] = patch
        return list(merged.values())
