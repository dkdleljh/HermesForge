from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Evidence, LambdaPatch, RenderedEvent, Snapshot


class EvidenceRepository(ABC):
    @abstractmethod
    def create(self, evidence: Evidence) -> Evidence:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Evidence]:
        raise NotImplementedError

    @abstractmethod
    def get(self, evidence_id: str) -> Optional[Evidence]:
        raise NotImplementedError


class PatchRepository(ABC):
    @abstractmethod
    def create(self, patch: LambdaPatch) -> LambdaPatch:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[LambdaPatch]:
        raise NotImplementedError

    @abstractmethod
    def get(self, patch_id: str) -> Optional[LambdaPatch]:
        raise NotImplementedError


class SnapshotRepository(ABC):
    @abstractmethod
    def create(self, snapshot: Snapshot) -> Snapshot:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Snapshot]:
        raise NotImplementedError

    @abstractmethod
    def get(self, snapshot_id: str) -> Optional[Snapshot]:
        raise NotImplementedError


class RenderedEventRepository(ABC):
    @abstractmethod
    def create(self, event: RenderedEvent) -> RenderedEvent:
        raise NotImplementedError

    @abstractmethod
    def list_recent(self, limit: int = 10) -> List[RenderedEvent]:
        raise NotImplementedError
