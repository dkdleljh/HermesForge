from pydantic import BaseModel


class DemoBootstrapResponse(BaseModel):
    message: str
    evidence_count: int
    patch_count: int
    snapshot_count: int
