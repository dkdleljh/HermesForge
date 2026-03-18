from app.domain.entities import Context


class NeuralContextInterface:
    """
    Phase 9: 뇌-컴퓨터 인터페이스(BCI)를 통해
    최고 관리자의 무의식적 뇌파를 실시간 의도(Intent)로 변환하는 모듈.
    """

    def translate_brainwave(self, raw_signal: float) -> str:
        """가상의 뇌파 신호(0.0~1.0)를 시스템 인텐트로 변환"""
        if raw_signal > 0.8:
            return "emergency_override"  # 극도의 긴장/위험 감지
        elif raw_signal < 0.2:
            return "standby"  # 극도의 이완
        else:
            return "analyze_tactical"  # 집중 및 분석 상태

    def inject_neural_intent(self, base_context: Context, raw_signal: float) -> Context:
        """기존 Context를 뇌파 기반 의도로 실시간 덮어씌움"""
        intent = self.translate_brainwave(raw_signal)
        base_context.intent = intent
        base_context.state_flags["bci_active"] = True
        return base_context
