from __future__ import annotations

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.service.thinking_extractor import ThinkingExtractor


class ExtractThinkingUseCase:
    def __init__(self, thinking_extractor: ThinkingExtractor) -> None:
        self._thinking_extractor = thinking_extractor

    def execute(self, draft: Draft) -> ExtractedThinking:
        return self._thinking_extractor.extract(draft)
