from app.engine.chaos import ChaosEngine
from random import Random
from typing import List, Tuple

from app.domain.entities import Context, LambdaPatch, Snapshot
from app.engine.interfaces import Materializer
from app.utils.hash_utils import stable_hash


class ContextAwareMaterializer(Materializer):
    """Context를 반영해 deterministic/weighted 결과를 선택한다."""

    def materialize(self, snapshot: Snapshot, context: Context, patches: List[LambdaPatch], mode: str) -> LambdaPatch:
        return BayesianNetworkMaterializer().materialize(snapshot, context, patches, mode)


class BayesianNetworkMaterializer(Materializer):
    """복잡계 다변수 확률 추론(Fuzzy/Bayesian)과 ChaosEngine을 결합하여 결과를 렌더링한다."""
    def __init__(self, chaos_engine: "ChaosEngine" = None): # type: ignore
        self.chaos_engine = chaos_engine

    def materialize(self, snapshot: Snapshot, context: Context, patches: List[LambdaPatch], mode: str) -> LambdaPatch:
        if not patches:
            raise ValueError("snapshot에 적용 가능한 patch가 없습니다")

        scored: List[Tuple[LambdaPatch, float]] = []
        import math
        for patch in patches:



            # 기본 확률은 선형곱이 아닌 비선형 신뢰도 지표를 따름
            base_score = patch.probability_mass * (patch.confidence ** 0.8)
            
            # Fuzzy 로직: 환경(Environment)과 의도(Intent)에 따른 지수함수적 증폭/감쇄
            multiplier = 1.0
            
            if context.environment == "high_risk":
                multiplier *= 1.8 if patch.outcome.get("category") in ["disaster", "training", "risk"] else 0.8
            
            if context.intent and context.intent in str(patch.outcome):
                multiplier *= math.exp(0.5)  # 강력한 동조 효과
                
            if context.scenario_profile in patch.labels:
                multiplier *= 1.3
                
            score = base_score * multiplier
            
            # ChaosEngine(나비효과) 적용: entropy_budget 만큼 노이즈 섞기
            if self.chaos_engine:
                score = self.chaos_engine.apply_noise(score, snapshot.entropy_budget)
                
            scored.append((patch, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        if mode == "deterministic":
            return scored[0][0]

        seed = int(stable_hash({"snapshot": snapshot.snapshot_id, "context": context.__dict__})[:8], 16)
        rng = Random(seed)
        total = sum(item[1] for item in scored)
        threshold = rng.uniform(0, total)
        current = 0.0
        for patch, score in scored:
            current += score
            if current >= threshold:
                return patch
        return scored[-1][0]
