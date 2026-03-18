from app.engine.chaos import ChaosEngine
from uuid import uuid4

from app.domain.entities import Context, RenderedEvent
from app.engine.materializer import BayesianNetworkMaterializer
from app.policies.safety_kernel import SafetyKernel
from app.repositories.base import PatchRepository, RenderedEventRepository, SnapshotRepository
from app.schemas.materialize import MaterializeRequest
from app.utils.hash_utils import stable_hash
from app.utils.time_utils import utc_now_iso


class MaterializeService:
    def __init__(self, snapshot_repo: SnapshotRepository, patch_repo: PatchRepository, rendered_repo: RenderedEventRepository):
        self.snapshot_repo = snapshot_repo
        self.patch_repo = patch_repo
        self.rendered_repo = rendered_repo
        self.chaos_engine = ChaosEngine()
        self.materializer = BayesianNetworkMaterializer(self.chaos_engine)
        self.safety = SafetyKernel()

    def materialize(self, req: MaterializeRequest) -> RenderedEvent:
        snapshot = self.snapshot_repo.get(req.snapshot_id)
        if not snapshot:
            raise ValueError("snapshot을 찾을 수 없습니다")

        patches = [self.patch_repo.get(pid) for pid in snapshot.patches]
        valid_patches = [patch for patch in patches if patch]
        context = Context(**req.context.model_dump())

        selected = self.materializer.materialize(snapshot, context, valid_patches, req.mode)
        context_hash = stable_hash(context.__dict__)

        event = RenderedEvent(
            render_id=f"re-{uuid4().hex[:12]}",
            snapshot_id=snapshot.snapshot_id,
            context_hash=context_hash,
            rendered_event={
                "category": selected.outcome.get("category", "general"),
                "action": selected.outcome.get("action", "hold"),
                "message": selected.outcome.get("message", "가능역 렌더 결과"),
                "mode": req.mode,
                "constraints": selected.constraint_proof,
                "confidence": selected.confidence,
            },
            confidence=selected.confidence,
            policy_hash=snapshot.policy_root,
            provenance={
                "patch_id": selected.id,
                "witness_refs": selected.witness_refs,
                "source_type": "pending",
            },
            label="pending",
            timestamp=utc_now_iso(),
        )

        safe_event = self.safety.apply(event, context.permissions)
        return self.rendered_repo.create(safe_event)

    def list_recent(self, limit: int = 10):
        return self.rendered_repo.list_recent(limit=limit)
