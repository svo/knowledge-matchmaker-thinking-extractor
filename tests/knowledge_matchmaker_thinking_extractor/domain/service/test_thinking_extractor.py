from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.service.thinking_extractor import ThinkingExtractor


class ConcreteThinkingExtractor(ThinkingExtractor):
    def extract(self, draft: Draft) -> ExtractedThinking:
        return ExtractedThinking(positions=[])


class TestThinkingExtractor:
    def test_should_be_abstract_base_class(self):
        assert_that(ThinkingExtractor.__abstractmethods__).contains("extract")

    def test_should_allow_concrete_implementation(self):
        extractor = ConcreteThinkingExtractor()

        result = extractor.extract(Draft(text="test"))

        assert_that(result.positions).is_empty()
