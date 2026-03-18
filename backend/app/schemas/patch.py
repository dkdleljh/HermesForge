from typing import Any, Dict, List

from pydantic import BaseModel, Field


class LambdaPatchCreate(BaseModel):
    conditions: Dict[str, Any]
    outcome: Dict[str, Any]
    probability_mass: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    constraint_proof: str
    witness_refs: List[str] = []
    anchor_weight: float = Field(default=1.0, ge=0.0)
    labels: List[str] = []


class LambdaPatchRead(BaseModel):
    id: str
    conditions: Dict[str, Any]
    outcome: Dict[str, Any]
    probability_mass: float
    confidence: float
    constraint_proof: str
    witness_refs: List[str]
    anchor_weight: float
    labels: List[str]
