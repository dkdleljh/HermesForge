from typing import List, Optional
from pydantic import BaseModel, Field

class SnapshotGenerateRequest(BaseModel):
    parent_snapshot_id: Optional[str] = None
    evidence_ids: List[str] = []
    patch_ids: List[str] = []
    entropy_budget: float = Field(default=1.0, ge=0.0)

class SnapshotMergeRequest(BaseModel):
    left_snapshot_id: str
    right_snapshot_id: str

class SnapshotRead(BaseModel):
    snapshot_id: str
    parent_snapshot_id: Optional[str]
    patches: List[str]
    policy_root: str
    witness_root: str
    entropy_budget: float
    created_at: str
    version: str
    duration: Optional[int] = None
