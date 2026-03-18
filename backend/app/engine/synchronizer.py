from typing import List
from app.domain.entities import RenderedEvent
from app.engine.actuator import Actuator


class RealitySynchronizer:
    """
    QuantumMerger를 통해 도출된 '최적의 미래(Golden Path)'를 받아,
    해당 시나리오를 물리적 현실로 만들기 위해 Actuator를 구동시키는 동기화 엔진.
    """

    def __init__(self, actuator: Actuator):
        self.actuator = actuator

    def sync_golden_path_to_reality(self, golden_path: List[RenderedEvent]) -> bool:
        """
        가장 이상적인 미래의 이벤트 목록을 순차적으로 현실 세계에 덮어씌움(Write).
        """
        if not golden_path:
            return False

        success_count = 0
        for event in golden_path:
            # 안전 커널이 REALITY_CONTROL 모드로 격상된 이벤트인지 확인 (이중 보안)
            if event.label != "REALITY_CONTROL":
                continue

            category = event.rendered_event.get("category", "")
            action = event.rendered_event.get("action", "")

            target_system = "unknown"
            command_params = {"render_id": event.render_id}

            if category == "disaster" and action == "priority_evacuation":
                target_system = "traffic_lights"
                command_params["route"] = "evacuation_path_A"
                command_params["signal"] = "force_green"

            elif category == "security" and action == "lockdown":
                target_system = "building_door_lock"
                command_params["state"] = "locked"

            # 매핑된 물리적 시스템이 있다면 액추에이터 구동
            if target_system != "unknown":
                if self.actuator.execute_command(target_system, action, command_params):
                    success_count += 1

        return success_count > 0
