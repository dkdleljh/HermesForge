import pytest
import asyncio
from app.domain.entities import Context, SimulationAgent
from app.engine.timeline import TimelineEngine
from app.engine.distributed_worker import ScaleOutWorkerPool
from app.schemas.snapshot import SnapshotGenerateRequest
from app.services.materialize_service import MaterializeService
from app.services.snapshot_service import SnapshotService
from app.core.container import get_unit
from app.repositories.sqlite import (
    SQLiteEvidenceRepository,
    SQLitePatchRepository,
    SQLiteRenderedEventRepository,
    SQLiteSnapshotRepository,
)


@pytest.fixture
def worker_pool():
    unit = get_unit()
    ev_repo = SQLiteEvidenceRepository(unit)
    patch_repo = SQLitePatchRepository(unit)
    snap_repo = SQLiteSnapshotRepository(unit)
    ren_repo = SQLiteRenderedEventRepository(unit)

    # 3개의 브랜치를 처리할 3개의 워커 노드 생성
    pool = ScaleOutWorkerPool(num_workers=3)

    for _ in range(3):
        snap_svc = SnapshotService(ev_repo, patch_repo, snap_repo)
        mat_svc = MaterializeService(snap_repo, patch_repo, ren_repo)
        engine = TimelineEngine(mat_svc, snap_svc)
        # 더미 에이전트 주입
        engine.register_agent(
            SimulationAgent(id="npc-test", name="Tester", state="idle", properties={})
        )
        pool.register_engine_node(engine)

    return pool, SnapshotService(ev_repo, patch_repo, snap_repo)


@pytest.mark.asyncio
async def test_multiverse_branching_and_quantum_merger(worker_pool):
    pool, snap_svc = worker_pool

    # 1. 초기 단일 스냅샷 발급
    init_snap = snap_svc.generate(SnapshotGenerateRequest(entropy_budget=1.0))

    # 2. 하나의 상황(Context)에서 3가지 다른 의도(Intent)로 분기 (평행 우주 3개 생성)
    base_ctx = Context(
        "commander", "high_risk", ["render"], {}, "disaster_response", "idle"
    )
    branching_intents = [
        "ignore",  # 무시 (최악의 결과 예상)
        "wait_for_backup",  # 대기 (중간 결과 예상)
        "priority_evacuation",  # 즉각 대피 (최적의 Golden Path 예상)
    ]

    # 3. 비동기 다중 우주 렌더링 및 Quantum Merger 평가 실행
    result = await pool.run_multiverse_branching(
        initial_snapshot_id=init_snap.snapshot_id,
        base_context=base_ctx,
        branching_intents=branching_intents,
        ticks=2,
    )

    # 4. 검증
    assert result["total_branches"] == 3
    assert len(result["all_results"]) == 3
    assert len(result["golden_path"]) == 2  # 2 Ticks
    assert result["best_score"] > 0  # 정상적으로 채점되었는지 확인
