import random
import math


class ChaosEngine:
    """현실의 예측 불가능성을 시뮬레이션에 주입하기 위한 혼돈 이론 엔진"""

    def apply_noise(self, base_score: float, entropy_budget: float) -> float:
        """
        주어진 점수에 가우시안 노이즈(정규 분포 난수)를 추가하여 나비효과 유도
        :param base_score: 베이지안/퍼지 모델을 통해 산출된 기본 확률 점수
        :param entropy_budget: 현재 시뮬레이션 스냅샷에 남아있는 불확실성 예산 (0.0 ~ 1.0)
        :return: 노이즈가 섞인 최종 점수
        """
        # entropy_budget이 클수록 노이즈의 표준편차(변동성)가 커짐
        volatility = max(0.01, entropy_budget * 0.5)

        # 평균 1.0, 표준편차가 volatility인 가우시안 노이즈
        noise_multiplier = random.gauss(mu=1.0, sigma=volatility)

        # 점수가 음수가 되지 않도록 최소 1% 보장
        final_score = max(base_score * 0.01, base_score * noise_multiplier)
        return final_score
