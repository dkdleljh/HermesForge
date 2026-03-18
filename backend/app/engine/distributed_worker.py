from app.engine.quantum_merger import QuantumMerger
import asyncio
from typing import List

from app.domain.entities import Context, Snapshot
from app.engine.timeline import TimelineEngine


class ScaleOutWorkerPool:
    """향후 수백만 개의 변수가 얽힌 나비효과 엔진을 Kubernetes 등으로 분산 처리하기 위한 모의 스캐폴드"""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.timeline_engines: List[TimelineEngine] = []

    def register_engine_node(self, engine: TimelineEngine):
        """Worker 노드에 타임라인 엔진 주입"""
        self.timeline_engines.append(engine)

    async def run_distributed_simulations(
        self, initial_snapshot_id: str, context: Context, ticks: int = 100
    ):
        """
        비동기 코루틴을 통해 수많은 시계열 시나리오를 병렬로 렌더링.
        각 Worker Node는 약간씩 다른 초기 난수 시드나 Context를 받아 분산 렌더링을 수행함.
        """
        if not self.timeline_engines:
            raise RuntimeError("등록된 Worker Node가 없습니다.")

        tasks = []
        for i, engine in enumerate(self.timeline_engines):
            # 복제된 독립적 Context (나비효과 테스트용 미세 조작)
            node_context = Context(
                user_role=context.user_role,
                environment=context.environment,
                permissions=context.permissions.copy(),
                state_flags={**context.state_flags, "worker_node_id": i},
                scenario_profile=context.scenario_profile,
                intent=context.intent,
            )

            # 동기 메서드를 스레드풀로 돌리거나 향후 async로 완전히 포팅 (여기서는 모의 실행)
            task = asyncio.to_thread(
                engine.run_simulation, initial_snapshot_id, node_context, ticks
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results
    async def run_multiverse_branching(
        self, initial_snapshot_id: str, base_context: Context, branching_intents: List[str], ticks: int = 3
    ):
        """
        단일 스냅샷에서 사용자의 여러 가지 결정(Intent 분기)에 따라 평행 우주를 생성하여 동시 렌더링 후,
        QuantumMerger를 통해 최적의 미래(Golden Path)를 역산한다.
        """
        if len(self.timeline_engines) < len(branching_intents):
            raise RuntimeError("분기(Branch) 수보다 Worker Node의 수가 부족합니다.")

        tasks = []
        for i, intent in enumerate(branching_intents):
            engine = self.timeline_engines[i]
            
            # 각 우주마다 다른 선택(Intent)을 한 것으로 Context 분기 (Git Branching)
            branched_context = Context(
                user_role=base_context.user_role,
                environment=base_context.environment,
                permissions=base_context.permissions.copy(),
                state_flags={**base_context.state_flags, "multiverse_branch_id": f"branch-{i}"},
                scenario_profile=base_context.scenario_profile,
                intent=intent,  # 핵심 분기점
            )

            task = asyncio.to_thread(
                engine.run_simulation, initial_snapshot_id, branched_context, ticks
            )
            tasks.append(task)

        # 1. 병렬 렌더링 진행
        multiverse_results = await asyncio.gather(*tasks)
        
        # 2. 양자 병합기를 통한 최적 시나리오(Golden Path) 계산
        merger = QuantumMerger()
        golden_path, best_score = merger.find_golden_path(multiverse_results)
        
        return {
            "total_branches": len(branching_intents),
            "golden_path": golden_path,
            "best_score": best_score,
            "all_results": multiverse_results
        }
