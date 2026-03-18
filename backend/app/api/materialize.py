from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_materialize_service
from app.schemas.materialize import MaterializeRequest, RenderedEventRead
from app.services.materialize_service import MaterializeService

router = APIRouter(prefix="", tags=["materialize"])


@router.post("/materialize", response_model=RenderedEventRead)
def materialize(payload: MaterializeRequest, service: MaterializeService = Depends(get_materialize_service)):
    try:
        return service.materialize(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/renders", response_model=List[RenderedEventRead])
def list_recent_renders(service: MaterializeService = Depends(get_materialize_service)):
    return service.list_recent(limit=20)
