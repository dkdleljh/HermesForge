import pytest
from app.domain.entities import Context, SimulationAgent
from app.engine.timeline import TimelineEngine
from app.schemas.snapshot import SnapshotGenerateRequest
from app.services.materialize_service import MaterializeService
from app.services.snapshot_service import SnapshotService
from app.core.container import get_evidence_service, get_patch_service, get_unit
from app.repositories.sqlite import (
    SQLiteEvidenceRepository,
    SQLitePatchRepository,
    SQLiteRenderedEventRepository,
    SQLiteSnapshotRepository,
)


@pytest.fixture
def timeline_services():
    unit = get_unit()
    ev_repo = SQLiteEvidenceRepository(unit)
    patch_repo = SQLitePatchRepository(unit)
    snap_repo = SQLiteSnapshotRepository(unit)
    ren_repo = SQLiteRenderedEventRepository(unit)

    snap_svc = SnapshotService(ev_repo, patch_repo, snap_repo)
    mat_svc = MaterializeService(snap_repo, patch_repo, ren_repo)
    return snap_svc, mat_svc


def test_timeline_engine_continuous_loop(timeline_services):
    snap_svc, mat_svc = timeline_services

    engine = TimelineEngine(mat_svc, snap_svc)

    # 1. 초기 더미 스냅샷 생성
    init_snap = snap_svc.generate(SnapshotGenerateRequest(entropy_budget=1.0))

    # 2. 다중 에이전트 생성
    agent1 = SimulationAgent(
        id="npc-1", name="Civilian A", state="idle", properties={"hp": 100}
    )
    agent2 = SimulationAgent(
        id="npc-2", name="Commander B", state="alert", properties={"auth": "high"}
    )
    engine.register_agent(agent1)
    engine.register_agent(agent2)

    # 3. 렌더링 컨텍스트 (3 Tick 연속 시뮬레이션)
    ctx = Context("trainer", "high_risk", ["render"], {}, "training", "simulate")
    history = engine.run_simulation(
        initial_snapshot_id=init_snap.snapshot_id, context=ctx, ticks=3
    )

    # 4. 검증
    assert len(history) == 3  # 3번의 타임라인 연쇄 루프 렌더링이 이루어져야 함
    assert history[0].render_id != history[1].render_id
    assert history[0].snapshot_id == init_snap.snapshot_id
    assert (
        history[1].snapshot_id != init_snap.snapshot_id
    )  # 결과가 원인이 되어 새로운 스냅샷 ID 파생

    # 에이전트 피드백 갱신 확인
    assert len(engine.agents["npc-1"].base_agent.history) == 3
    assert "last_action" in engine.agents["npc-2"].base_agent.properties
