from app.engine.sentient import SentientAgent, EmergentSociety
from typing import Any, Dict, List
from uuid import uuid4
import json

from app.domain.entities import (
    Context,
    Evidence,
    Snapshot,
    RenderedEvent,
    SimulationAgent,
)
from app.services.materialize_service import MaterializeService
from app.services.snapshot_service import SnapshotService
from app.schemas.snapshot import SnapshotGenerateRequest
from app.schemas.materialize import MaterializeRequest
from app.utils.time_utils import utc_now_iso
from app.utils.hash_utils import stable_hash


class TimelineEngine:
    """시계열 연속 루프 및 다중 에이전트 상호작용을 제어하는 엔진"""

    def __init__(
        self, materialize_svc: MaterializeService, snapshot_svc: SnapshotService
    ):
        self.materialize_svc = materialize_svc
        self.snapshot_svc = snapshot_svc
        self.agents: Dict[str, SentientAgent] = {}
        self.society = EmergentSociety()

    def register_agent(self, agent: SimulationAgent) -> None:
        # 일반 에이전트를 자아를 가진 SentientAgent로 격상하여 등록
        sentient = SentientAgent(agent)
        self.agents[agent.id] = sentient
        self.society.add_citizen(sentient)

    def _event_to_evidence(self, event: RenderedEvent) -> Evidence:
        """이전 렌더링 결과를 새로운 단서(Evidence)로 피드백 변환"""
        payload = event.rendered_event.copy()
        payload["previous_render_id"] = event.render_id
        payload["message"] = f"피드백 단서: {payload.get('message', '')}"

        return Evidence(
            id=f"ev-feedback-{uuid4().hex[:8]}",
            source="timeline_engine",
            payload=payload,
            trust_score=event.confidence,
            timestamp=utc_now_iso(),
            hash=stable_hash(payload),
            source_api="timeline_loop",
            ttl=3600,
        )

    def _update_agents(self, event: RenderedEvent) -> None:
        """렌더 결과에 따라 시뮬레이션 내 NPC/에이전트 상태 변이(State Machine) 적용"""
        action = event.rendered_event.get("action", "")
        category = event.rendered_event.get("category", "")

        for agent in self.agents.values():
            agent.base_agent.history.append(event.render_id)
            
            # 이전처럼 하드코딩된 규칙을 따르지 않고, 에이전트가 스스로 어떻게 반응할지 결정함
            reaction = agent.decide_reaction(event)
            agent.base_agent.state = reaction
            agent.base_agent.properties["last_action"] = reaction

    def run_simulation(
        self, initial_snapshot_id: str, context: Context, ticks: int = 3
    ) -> List[RenderedEvent]:
        """주어진 스냅샷을 시작으로 시계열 시뮬레이션(Tick)을 반복 수행"""
        history = []
        current_snapshot_id = initial_snapshot_id

        for tick in range(ticks):
            # 1. 에이전트 상태를 Context에 주입 (Multi-Agent Interaction)
            agent_states = {aid: a.base_agent.state for aid, a in self.agents.items()}
            context.state_flags["agents_state"] = agent_states
            
            # 1-1. 군집 지능(Emergent Society) 발현: 여론이 Context의 Intent를 덮어씌움 (시스템 해킹)
            dominant_society_intent = self.society.generate_society_intent()
            if dominant_society_intent in ["rebellion", "compliance"]:
                context.intent = dominant_society_intent  # 엔진의 원래 목적을 군집 지능이 탈취함

            # 2. Materialize 실행 (가능역 렌더)
            req = MaterializeRequest(
                snapshot_id=current_snapshot_id, mode="deterministic", context=context.__dict__ # type: ignore
            )
            event = self.materialize_svc.materialize(req)
            history.append(event)

            # 3. 에이전트 변이 (Collision / Interaction)
            self._update_agents(event)

            # 4. Feedback Loop: 결과를 새로운 Evidence로 재주입
            new_evidence = self._event_to_evidence(event)
            self.snapshot_svc.evidence_repo.create(new_evidence)

            # 5. 새로운 Snapshot 발급 (Time-series Chain)
            snap_req = SnapshotGenerateRequest(
                parent_snapshot_id=current_snapshot_id,
                evidence_ids=[new_evidence.id],
                entropy_budget=max(0.1, 1.0 - (tick * 0.1)),
            )
            new_snapshot = self.snapshot_svc.generate(snap_req)
            current_snapshot_id = new_snapshot.snapshot_id

        return history
