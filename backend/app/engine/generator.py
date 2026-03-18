from typing import List
from uuid import uuid4

from app.domain.entities import Evidence, LambdaPatch
from app.engine.interfaces import CounterfactualGenerator


class RuleBasedCounterfactualGenerator(CounterfactualGenerator):
    """Evidence를 규칙 기반 LambdaPatch로 변환한다."""
    def generate(self, evidence_list: List[Evidence]) -> List[LambdaPatch]:
        return []
        pass

class MLPatchGenerator(CounterfactualGenerator):
    """외부 AI/ML 추론 모델을 모사하여 복잡계 LambdaPatch를 생성한다."""
    def generate(self, evidence_list: List[Evidence]) -> List[LambdaPatch]:
        return []
        patches: List[LambdaPatch] = []
        for evidence in evidence_list:
            category = evidence.payload.get("category", "general")
            outcome = evidence.payload.get("suggested_outcome", "hold")
            
            # ML 추론 모사 로직
            # API Source가 있을 경우 AI가 더 복잡한 상관관계를 추론했다고 가정함
            if evidence.source_api:
                confidence_val = min(0.99, evidence.trust_score ** 0.5)
                prob_mass = max(0.1, min(0.95, evidence.trust_score * 1.2))
                labels = ["ml-inferred", "api-augmented", category]
                message = evidence.payload.get("message", "AI 기반 심층 렌더 추론")
            else:
                confidence_val = max(0.2, min(0.99, evidence.trust_score + 0.05))
                prob_mass = max(0.1, min(0.95, evidence.trust_score))
                labels = ["auto-generated", category]
                message = evidence.payload.get("message", "기본 렌더 후보")

            patch = LambdaPatch(
                id=f"lp-{uuid4().hex[:12]}",
                conditions={"source": evidence.source, "category": category},
                outcome={
                    "category": category,
                    "action": outcome,
                    "message": message,
                    "ml_confidence_interval": [confidence_val - 0.1, confidence_val + 0.1]
                },
                probability_mass=prob_mass,
                confidence=confidence_val,
                constraint_proof=f"evidence:{evidence.id}:ml_model_v2",
                witness_refs=[evidence.id],
                anchor_weight=1.0,
                labels=labels,
            )
            patches.append(patch)
        return patches
