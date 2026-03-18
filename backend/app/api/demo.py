from fastapi import APIRouter, Depends

from app.api.deps import get_demo_service
from app.schemas.demo import DemoBootstrapResponse
from app.services.demo_service import DemoService

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/bootstrap", response_model=DemoBootstrapResponse)
def bootstrap(service: DemoService = Depends(get_demo_service)):
    return service.bootstrap()
