from typing import Any, Dict

from app.domain.entities import RenderedEvent
from app.utils.hash_utils import stable_hash


class SafetyKernel:
    """출력 안전 정책을 강제하는 커널."""

    policy_name = "HermesForge-SafetyKernel"
    policy_version = "0.1.0"

    def apply(self, event: RenderedEvent, context_permissions: list | None = None) -> RenderedEvent:
        if event.confidence is None:
            raise ValueError("confidence 없는 출력은 금지됩니다")

        # 7단계 현실 동기화(Actuation) 특권 모드 확인
        if context_permissions and "execute_reality_control" in context_permissions:
            event.label = "REALITY_CONTROL"
            event.provenance["source_type"] = "physical_actuation_command"
            event.provenance["watermark"] = "ACTUAL_FACT_TRIGGER"
            event.provenance["notice"] = "[경고] 본 출력은 현실 세계의 물리적 자산을 직접 제어합니다."
        else:
            # 기본 시뮬레이션 모드
            event.label = "POSSIBILITY_RENDER"
            event.provenance["source_type"] = "non_factual_projection"
        event.provenance["watermark"] = "NOT_FACT"
        event.provenance["notice"] = "본 출력은 사실 기록이 아닌 가능역 렌더입니다."

        if not event.policy_hash:
            event.policy_hash = stable_hash({"policy": self.policy_name, "version": self.policy_version})

        dangerous = event.rendered_event.get("category") in {"harmful", "illegal"}
        if dangerous:
            raise ValueError("위험 category 결과는 외부화할 수 없습니다")

        if "confidence" not in event.rendered_event:
            event.rendered_event["confidence"] = event.confidence

        return event

    def rules(self) -> Dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "version": self.policy_version,
            "rules": [
                {"code": "LABEL_ENFORCE", "description": "모든 렌더 결과에 POSSIBILITY_RENDER 라벨 강제"},
                {"code": "PROVENANCE_ENFORCE", "description": "provenance.source_type=non_factual_projection 강제"},
                {"code": "REQUIRE_CONFIDENCE", "description": "confidence 누락 시 출력 금지"},
                {"code": "REQUIRE_POLICY_HASH", "description": "policy_hash 누락 시 자동 생성"},
                {"code": "BLOCK_DANGEROUS", "description": "harmful/illegal category 외부화 차단"},
                {"code": "NOT_FACT_WATERMARK", "description": "NOT_FACT 워터마크 강제"},
            ],
        }
