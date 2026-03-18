from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, Field


class ApiMessage(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "HermesForge"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DictPayload(BaseModel):
    payload: Dict[str, Any]
