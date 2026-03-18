from functools import lru_cache

from app.core.config import get_settings
from app.plugins.registry import build_default_registry
from app.repositories.sqlite import (
    SQLiteEvidenceRepository,
    SQLitePatchRepository,
    SQLiteRenderedEventRepository,
    SQLiteSnapshotRepository,
    SQLiteUnit,
)
from app.services.demo_service import DemoService
from app.services.evidence_service import EvidenceService
from app.services.materialize_service import MaterializeService
from app.services.patch_service import PatchService
from app.services.policy_service import PolicyService
from app.services.snapshot_service import SnapshotService


@lru_cache
def get_unit() -> SQLiteUnit:
    settings = get_settings()
    return SQLiteUnit(settings.db_path)


@lru_cache
def get_evidence_service() -> EvidenceService:
    repo = SQLiteEvidenceRepository(get_unit())
    return EvidenceService(repo)


@lru_cache
def get_patch_service() -> PatchService:
    repo = SQLitePatchRepository(get_unit())
    return PatchService(repo)


@lru_cache
def get_snapshot_service() -> SnapshotService:
    return SnapshotService(SQLiteEvidenceRepository(get_unit()), SQLitePatchRepository(get_unit()), SQLiteSnapshotRepository(get_unit()))


@lru_cache
def get_materialize_service() -> MaterializeService:
    return MaterializeService(SQLiteSnapshotRepository(get_unit()), SQLitePatchRepository(get_unit()), SQLiteRenderedEventRepository(get_unit()))


@lru_cache
def get_policy_service() -> PolicyService:
    return PolicyService()


@lru_cache
def get_demo_service() -> DemoService:
    return DemoService(get_evidence_service(), get_snapshot_service(), build_default_registry())
