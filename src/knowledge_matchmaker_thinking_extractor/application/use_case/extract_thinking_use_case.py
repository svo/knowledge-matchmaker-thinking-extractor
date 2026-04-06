from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.port.thinking_extractor_port import ThinkingExtractorPort


class ExtractThinkingUseCase:
    def __init__(self, extractor: ThinkingExtractorPort) -> None:
        self._extractor = extractor

    def execute(self, draft: Draft) -> ExtractedThinking:
        return self._extractor.extract(draft)
