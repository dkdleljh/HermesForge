from fastapi import APIRouter

from app.api import demo, evidence, health, materialize, patches, policies, snapshots, visualizer

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(evidence.router)
api_router.include_router(patches.router)
api_router.include_router(snapshots.router)
api_router.include_router(materialize.router)
api_router.include_router(policies.router)
api_router.include_router(demo.router)
api_router.include_router(visualizer.router, prefix="/visualizer", tags=["visualizer"])
