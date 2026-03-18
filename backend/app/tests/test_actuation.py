import pytest
from app.domain.entities import RenderedEvent
from app.engine.actuator import SmartCityActuator
from app.engine.synchronizer import RealitySynchronizer


def test_reality_synchronizer_actuation():
    # 1. 엑추에이터 및 동기화 엔진 초기화
    actuator = SmartCityActuator()
    synchronizer = RealitySynchronizer(actuator)

    # 2. 일반 시뮬레이션 이벤트 (권한 없음)
    normal_event = RenderedEvent(
        render_id="re-normal",
        snapshot_id="ss-1",
        context_hash="ctx",
        rendered_event={"category": "disaster", "action": "priority_evacuation"},
        confidence=0.9,
        policy_hash="pol",
        provenance={},
        label="POSSIBILITY_RENDER",
        timestamp="now",
    )

    # 3. 권한이 격상된 현실 개입 이벤트 (execute_reality_control 보유)
    god_mode_event = RenderedEvent(
        render_id="re-god",
        snapshot_id="ss-1",
        context_hash="ctx",
        rendered_event={"category": "disaster", "action": "priority_evacuation"},
        confidence=0.9,
        policy_hash="pol",
        provenance={},
        label="REALITY_CONTROL",
        timestamp="now",
    )

    # 4. Golden Path 실행 (일반 1개, 현실제어 1개)
    golden_path = [normal_event, god_mode_event]

    # 5. 동기화기 실행 및 결과 검증
    # 정상적인 경우, normal_event는 무시(skip)되고 god_mode_event 하나만 실제 Actuator를 구동시켜 True를 반환해야 함.
    success = synchronizer.sync_golden_path_to_reality(golden_path)

    assert success is True
