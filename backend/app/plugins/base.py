from abc import ABC, abstractmethod
from typing import Dict, List


class DomainPlugin(ABC):
    name: str

    @abstractmethod
    def sample_evidence(self) -> List[Dict]:
        raise NotImplementedError

    @abstractmethod
    def context_hint(self) -> Dict:
        raise NotImplementedError
