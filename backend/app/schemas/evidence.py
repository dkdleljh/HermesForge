from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class EvidenceCreate(BaseModel):
    source: str = Field(min_length=1)
    payload: Dict[str, Any]
    trust_score: float = Field(ge=0.0, le=1.0)
    timestamp: str
    source_api: Optional[str] = None
    ttl: Optional[int] = None

class EvidenceRead(BaseModel):
    id: str
    source: str
    payload: Dict[str, Any]
    trust_score: float
    timestamp: str
    hash: str
    source_api: Optional[str] = None
    ttl: Optional[int] = None
