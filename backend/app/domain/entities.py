from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Evidence:
    id: str
    source: str
    payload: Dict[str, Any]
    trust_score: float
    timestamp: str
    hash: str
    source_api: Optional[str] = None
    ttl: Optional[int] = None





@dataclass
class LambdaPatch:
    id: str
    conditions: Dict[str, Any]
    outcome: Dict[str, Any]
    probability_mass: float
    confidence: float
    constraint_proof: str
    witness_refs: List[str] = field(default_factory=list)
    anchor_weight: float = 1.0
    labels: List[str] = field(default_factory=list)


@dataclass
class Snapshot:
    snapshot_id: str
    parent_snapshot_id: Optional[str]
    patches: List[str]
    policy_root: str
    witness_root: str
    entropy_budget: float
    created_at: str
    version: str
    duration: Optional[int] = None







@dataclass
class SimulationAgent:
    id: str
    name: str
    state: str
    properties: Dict[str, Any]
    history: List[str] = field(default_factory=list)


@dataclass
class Context:
    user_role: str
    environment: str
    permissions: List[str]
    state_flags: Dict[str, Any]
    scenario_profile: str
    intent: str


@dataclass
class RenderedEvent:
    render_id: str
    snapshot_id: str
    context_hash: str
    rendered_event: Dict[str, Any]
    confidence: float
    policy_hash: str
    provenance: Dict[str, Any]
    label: str
    timestamp: str
