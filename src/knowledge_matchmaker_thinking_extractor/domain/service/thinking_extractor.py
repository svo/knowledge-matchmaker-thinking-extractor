from __future__ import annotations

from abc import ABC, abstractmethod

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking


class ThinkingExtractor(ABC):
    @abstractmethod
    def extract(self, draft: Draft) -> ExtractedThinking:
        pass
