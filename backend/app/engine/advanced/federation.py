from typing import List, Tuple
from app.domain.entities import RenderedEvent
from app.engine.quantum_merger import QuantumMerger


class ForgeFederation:
    """
    Phase 10: 다중 포지 연합.
    서로 다른 도시/국가의 HermesForge 노드들이 도출한 타임라인들을 교환하고,
    양측 모두 파국을 피하는 교집합(Win-win Golden Path)을 도출하는 협상 엔진.
    """

    def __init__(self, merger: QuantumMerger):
        self.merger = merger

    def negotiate(
        self,
        forge_a_proposals: List[List[RenderedEvent]],
        forge_b_proposals: List[List[RenderedEvent]],
    ) -> Tuple[List[RenderedEvent], float]:
        """
        A도시와 B도시의 Forge가 각각 수백 개의 타임라인을 제시하면,
        이를 병합하여 전체 생존율이 가장 높은 타임라인을 합의안으로 채택.
        """
        combined_proposals = forge_a_proposals + forge_b_proposals

        # QuantumMerger의 채점 로직을 재사용하여 글로벌 최적해 도출
        agreed_path, consensus_score = self.merger.find_golden_path(combined_proposals)

        return agreed_path, consensus_score
