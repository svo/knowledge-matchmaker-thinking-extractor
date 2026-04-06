from abc import ABC

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.port.thinking_extractor_port import ThinkingExtractorPort


class TestThinkingExtractorPort:
    def test_should_be_abstract_when_defined(self) -> None:
        assert_that(issubclass(ThinkingExtractorPort, ABC)).is_true()
