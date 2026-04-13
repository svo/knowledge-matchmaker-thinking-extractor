from __future__ import annotations

from unittest.mock import Mock

import pytest
from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import (
    ExtractThinkingUseCase,
)
from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType
from knowledge_matchmaker_thinking_extractor.domain.service.thinking_extractor import ThinkingExtractor


class TestExtractThinkingUseCase:
    @pytest.fixture
    def mock_thinking_extractor(self) -> Mock:
        return Mock(spec=ThinkingExtractor)

    @pytest.fixture
    def use_case(self, mock_thinking_extractor: Mock) -> ExtractThinkingUseCase:
        return ExtractThinkingUseCase(thinking_extractor=mock_thinking_extractor)

    @pytest.fixture
    def draft(self) -> Draft:
        return Draft(text="some draft text")

    @pytest.fixture
    def extracted_thinking(self) -> ExtractedThinking:
        return ExtractedThinking(positions=[Position(text="a claim", position_type=PositionType.CLAIM)])

    def test_should_call_extractor_with_draft(
        self,
        use_case: ExtractThinkingUseCase,
        mock_thinking_extractor: Mock,
        draft: Draft,
        extracted_thinking: ExtractedThinking,
    ) -> None:
        mock_thinking_extractor.extract.return_value = extracted_thinking

        use_case.execute(draft)

        mock_thinking_extractor.extract.assert_called_once_with(draft)

    def test_should_return_extracted_thinking(
        self,
        use_case: ExtractThinkingUseCase,
        mock_thinking_extractor: Mock,
        draft: Draft,
        extracted_thinking: ExtractedThinking,
    ) -> None:
        mock_thinking_extractor.extract.return_value = extracted_thinking

        result = use_case.execute(draft)

        assert_that(result).is_equal_to(extracted_thinking)
