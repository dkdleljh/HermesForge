from typing import List
from app.domain.entities import Evidence, Context
from app.engine.distributed_worker import ScaleOutWorkerPool
from app.engine.synchronizer import RealitySynchronizer


class AutoHealingDaemon:
    """
    Phase 8: 인간의 개입 없이 시스템이 배경에서 이상 현상(Anomaly)을 감지하고,
    즉각적으로 다중 우주 탐색을 거쳐 현실(Actuator)을 자동 패치하는 자가 치유 엔진.
    """

    def __init__(
        self, worker_pool: ScaleOutWorkerPool, synchronizer: RealitySynchronizer
    ):
        self.worker_pool = worker_pool
        self.synchronizer = synchronizer

    async def heal_anomaly(
        self, anomaly_evidence: Evidence, base_context: Context
    ) -> bool:
        # 이상 징후 감지 후 시스템이 자체적으로 여러 대처 방안(Intents)을 생성
        automated_intents = [
            "isolate_sector",
            "priority_evacuation",
            "deploy_emergency_drones",
            "wait_and_observe",
        ]

        # 관리자 권한 자동 부여 (자가 치유를 위한 시스템 특권)
        base_context.permissions.append("execute_reality_control")

        # 다중 우주 분기 렌더링을 통한 최적해(Golden Path) 탐색
        result = await self.worker_pool.run_multiverse_branching(
            initial_snapshot_id="ss-anomaly-detected",
            base_context=base_context,
            branching_intents=automated_intents,
            ticks=3,
        )

        golden_path = result.get("golden_path", [])

        # 인간의 승인 없이 즉각적으로 물리적 현실 개입(Actuation) 실행
        return self.synchronizer.sync_golden_path_to_reality(golden_path)
