from unittest.mock import Mock

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import ExtractThinkingUseCase
from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.port.thinking_extractor_port import ThinkingExtractorPort


class TestExtractThinkingUseCase:
    def test_should_call_extractor_when_executed(self) -> None:
        mock_extractor = Mock(spec=ThinkingExtractorPort)
        mock_extractor.extract.return_value = ExtractedThinking(claims=[], assumptions=[], framings=[])
        use_case = ExtractThinkingUseCase(extractor=mock_extractor)
        draft = Draft(text="test draft")

        use_case.execute(draft)

        mock_extractor.extract.assert_called_once_with(draft)

    def test_should_return_extracted_thinking_when_executed(self) -> None:
        mock_extractor = Mock(spec=ThinkingExtractorPort)
        expected = ExtractedThinking(claims=["claim"], assumptions=[], framings=[])
        mock_extractor.extract.return_value = expected
        use_case = ExtractThinkingUseCase(extractor=mock_extractor)
        draft = Draft(text="test draft")

        result = use_case.execute(draft)

        assert_that(result).is_equal_to(expected)
