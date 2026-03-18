from typing import Dict, List

from app.domain.entities import LambdaPatch
from app.engine.interfaces import Compressor


class SimplePatchCompressor(Compressor):
    """동일 action/category 조합의 patch를 대표 patch로 정규화한다."""

    def compress(self, patches: List[LambdaPatch]) -> List[LambdaPatch]:
        grouped: Dict[str, LambdaPatch] = {}
        for patch in patches:
            key = f"{patch.outcome.get('category')}::{patch.outcome.get('action')}"
            existing = grouped.get(key)
            if not existing or patch.confidence > existing.confidence:
                grouped[key] = patch
        return list(grouped.values())
