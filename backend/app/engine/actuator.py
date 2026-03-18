import logging


class Actuator:
    """물리적 현실 세계(IoT, 스마트 시티망 등)에 직접 명령을 내리는 액추에이터 인터페이스"""

    def execute_command(
        self, target_system: str, action: str, parameters: dict
    ) -> bool:
        raise NotImplementedError


class SmartCityActuator(Actuator):
    """가상의 스마트 시티 관제망 액추에이터"""

    def execute_command(
        self, target_system: str, action: str, parameters: dict
    ) -> bool:
        # 실제 환경에서는 MQTT나 외부 하드웨어 제어 API(REST)를 호출함.
        # 여기서는 로깅으로 모사.
        msg = f"[REALITY CONTROL] 시스템 '{target_system}'에 명령 '{action}' 하달. 매개변수: {parameters}"
        print(msg)
        logging.info(msg)
        return True
