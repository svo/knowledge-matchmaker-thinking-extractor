from __future__ import annotations

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType


class TestExtractedThinking:
    def test_should_have_positions(self) -> None:
        positions = [Position(text="a claim", position_type=PositionType.CLAIM)]
        extracted_thinking = ExtractedThinking(positions=positions)

        assert_that(extracted_thinking.positions).is_equal_to(positions)

    def test_should_have_empty_positions_by_default(self) -> None:
        extracted_thinking = ExtractedThinking()

        assert_that(extracted_thinking.positions).is_empty()
