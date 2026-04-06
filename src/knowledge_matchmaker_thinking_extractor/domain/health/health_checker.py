from abc import ABC, abstractmethod

from knowledge_matchmaker_thinking_extractor.domain.health.health_status import HealthResult


class HealthChecker(ABC):
    @abstractmethod
    def check_liveness(self) -> HealthResult:
        raise NotImplementedError()

    @abstractmethod
    def check_readiness(self) -> HealthResult:
        raise NotImplementedError()
