from abc import ABC, abstractmethod

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking


class ThinkingExtractorPort(ABC):
    @abstractmethod
    def extract(self, draft: Draft) -> ExtractedThinking:
        raise NotImplementedError
