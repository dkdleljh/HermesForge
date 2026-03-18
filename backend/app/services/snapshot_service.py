from typing import List
from uuid import uuid4

from app.domain.entities import Snapshot
from app.engine.compressor import SimplePatchCompressor
from app.engine.generator import MLPatchGenerator
from app.engine.merger import PolicyAwareMerger
from app.repositories.base import EvidenceRepository, PatchRepository, SnapshotRepository
from app.schemas.snapshot import SnapshotGenerateRequest, SnapshotMergeRequest
from app.utils.hash_utils import stable_hash
from app.utils.time_utils import utc_now_iso


class SnapshotService:
    def __init__(self, evidence_repo: EvidenceRepository, patch_repo: PatchRepository, snapshot_repo: SnapshotRepository):
        self.evidence_repo = evidence_repo
        self.patch_repo = patch_repo
        self.snapshot_repo = snapshot_repo
        self.generator = MLPatchGenerator()
        self.compressor = SimplePatchCompressor()
        self.merger = PolicyAwareMerger()

    def generate(self, req: SnapshotGenerateRequest) -> Snapshot:
        evidence_items = self.evidence_repo.list_all()
        if req.evidence_ids:
            wanted = set(req.evidence_ids)
            evidence_items = [item for item in evidence_items if item.id in wanted]

        generated = self.generator.generate(evidence_items)
        generated = self.compressor.compress(generated)

        manual_patches = self.patch_repo.list_all()
        if req.patch_ids:
            wanted_patch = set(req.patch_ids)
            manual_patches = [patch for patch in manual_patches if patch.id in wanted_patch]

        patch_ids = [patch.id for patch in [*manual_patches, *generated]]
        for patch in generated:
            self.patch_repo.create(patch)

        snapshot = Snapshot(
            snapshot_id=f"ss-{uuid4().hex[:12]}",
            parent_snapshot_id=req.parent_snapshot_id,
            patches=patch_ids,
            policy_root=stable_hash({"policy": "default", "version": "0.1.0"}),
            witness_root=stable_hash({"witness_refs": patch_ids}),
            entropy_budget=req.entropy_budget,
            created_at=utc_now_iso(),
            version="0.1.0",
        )
        return self.snapshot_repo.create(snapshot)

    def merge(self, req: SnapshotMergeRequest) -> Snapshot:
        left = self.snapshot_repo.get(req.left_snapshot_id)
        right = self.snapshot_repo.get(req.right_snapshot_id)
        if not left or not right:
            raise ValueError("병합 대상 snapshot을 찾을 수 없습니다")

        left_patches = [self.patch_repo.get(pid) for pid in left.patches]
        right_patches = [self.patch_repo.get(pid) for pid in right.patches]
        merged_patches = self.merger.merge(
            left,
            right,
            [patch for patch in left_patches if patch],
            [patch for patch in right_patches if patch],
        )

        snapshot = Snapshot(
            snapshot_id=f"ss-{uuid4().hex[:12]}",
            parent_snapshot_id=left.snapshot_id,
            patches=[patch.id for patch in merged_patches],
            policy_root=stable_hash({"left": left.policy_root, "right": right.policy_root}),
            witness_root=stable_hash({"left": left.witness_root, "right": right.witness_root}),
            entropy_budget=min(left.entropy_budget, right.entropy_budget),
            created_at=utc_now_iso(),
            version="0.1.0",
        )
        return self.snapshot_repo.create(snapshot)

    def list_all(self) -> List[Snapshot]:
        return self.snapshot_repo.list_all()

    def get(self, snapshot_id: str) -> Snapshot | None:
        return self.snapshot_repo.get(snapshot_id)
