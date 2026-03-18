from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_snapshot_service
from app.schemas.snapshot import SnapshotGenerateRequest, SnapshotMergeRequest, SnapshotRead
from app.services.snapshot_service import SnapshotService

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.post("/generate", response_model=SnapshotRead)
def generate_snapshot(payload: SnapshotGenerateRequest, service: SnapshotService = Depends(get_snapshot_service)):
    return service.generate(payload)


@router.get("", response_model=List[SnapshotRead])
def list_snapshots(service: SnapshotService = Depends(get_snapshot_service)):
    return service.list_all()


@router.get("/{snapshot_id}", response_model=SnapshotRead)
def get_snapshot(snapshot_id: str, service: SnapshotService = Depends(get_snapshot_service)):
    snapshot = service.get(snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="snapshot not found")
    return snapshot


@router.post("/merge", response_model=SnapshotRead)
def merge_snapshot(payload: SnapshotMergeRequest, service: SnapshotService = Depends(get_snapshot_service)):
    try:
        return service.merge(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
