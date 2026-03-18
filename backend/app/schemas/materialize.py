from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ContextInput(BaseModel):
    user_role: str
    environment: str
    permissions: List[str]
    state_flags: Dict[str, Any]
    scenario_profile: str
    intent: str


class MaterializeRequest(BaseModel):
    snapshot_id: str
    mode: str = Field(default="deterministic", pattern="^(deterministic|weighted)$")
    context: ContextInput


class RenderedEventRead(BaseModel):
    render_id: str
    snapshot_id: str
    context_hash: str
    rendered_event: Dict[str, Any]
    confidence: float
    policy_hash: str
    provenance: Dict[str, Any]
    label: str
    timestamp: str
