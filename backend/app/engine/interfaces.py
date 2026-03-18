from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Context, Evidence, LambdaPatch, Snapshot


class CounterfactualGenerator(ABC):
    @abstractmethod
    def generate(self, evidence_list: List[Evidence]) -> List[LambdaPatch]:
        raise NotImplementedError


class Compressor(ABC):
    @abstractmethod
    def compress(self, patches: List[LambdaPatch]) -> List[LambdaPatch]:
        raise NotImplementedError


class Materializer(ABC):
    @abstractmethod
    def materialize(self, snapshot: Snapshot, context: Context, patches: List[LambdaPatch], mode: str) -> LambdaPatch:
        raise NotImplementedError


class Merger(ABC):
    @abstractmethod
    def merge(self, left: Snapshot, right: Snapshot, left_patches: List[LambdaPatch], right_patches: List[LambdaPatch]) -> List[LambdaPatch]:
        raise NotImplementedError
