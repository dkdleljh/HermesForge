import random
from app.domain.entities import RenderedEvent
from app.policies.safety_kernel import SafetyKernel


class AdversarialSafetyKernel(SafetyKernel):
    """
    실무 과제 3 (GAN Security):
    자가 적대적 신경망(GAN) 기반으로 에이전트들의 교묘한 시스템 해킹 시도를 감지하고 방어하는 진화된 커널.
    """

    def apply(
        self, event: RenderedEvent, context_permissions: list | None = None
    ) -> RenderedEvent:
        # 1차 게이트: 기존 SafetyKernel의 정책 통과
        event = super().apply(event, context_permissions)

        # 2차 게이트: GAN 기반 맥락 이상 징후 판별 (Mocking)
        # 악의적 에이전트(SentientAgent)가 REALITY_CONTROL 권한을 교묘하게 탈취했는지 확률적으로 심문함
        anomaly_score = random.random()
        if (
            event.label == "REALITY_CONTROL" and anomaly_score > 0.95
        ):  # 5% 확률로 정교한 해킹 징후 적발
            event.label = "BLOCKED_BY_GAN"
            event.provenance["watermark"] = "THREAT_DETECTED"
            event.provenance["notice"] = (
                "[보안 경고] GAN 적대적망이 시스템 해킹 징후를 감지하여 물리 제어를 차단했습니다."
            )
            raise PermissionError(
                "AdversarialSafetyKernel: 악의적 현실 제어 시도 차단됨"
            )

        return event
