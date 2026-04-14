from __future__ import annotations

import pytest
from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType
from knowledge_matchmaker_thinking_extractor.interface.api.data_transfer_object.extract_thinking_data_transfer_object import (
    ExtractThinkingRequestDto,
    ExtractThinkingResponseDto,
)


class TestExtractThinkingRequestDto:
    def test_should_accept_draft_field(self) -> None:
        dto = ExtractThinkingRequestDto(draft="some draft text")

        assert_that(dto.draft).is_equal_to("some draft text")


class TestExtractThinkingResponseDto:
    @pytest.fixture
    def extracted_thinking_with_all_types(self) -> ExtractedThinking:
        return ExtractedThinking(
            positions=[
                Position(text="AI will transform education", position_type=PositionType.CLAIM),
                Position(text="Technology is neutral", position_type=PositionType.ASSUMPTION),
                Position(text="Progress narrative", position_type=PositionType.FRAMING),
            ]
        )

    @pytest.fixture
    def extracted_thinking_with_only_claims(self) -> ExtractedThinking:
        return ExtractedThinking(
            positions=[
                Position(text="first claim", position_type=PositionType.CLAIM),
                Position(text="second claim", position_type=PositionType.CLAIM),
            ]
        )

    def test_should_place_claim_text_in_claims_array_when_from_domain_model_is_called(
        self, extracted_thinking_with_all_types: ExtractedThinking
    ) -> None:
        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking_with_all_types)

        assert_that(dto.claims).is_equal_to(["AI will transform education"])

    def test_should_place_assumption_text_in_assumptions_array_when_from_domain_model_is_called(
        self, extracted_thinking_with_all_types: ExtractedThinking
    ) -> None:
        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking_with_all_types)

        assert_that(dto.assumptions).is_equal_to(["Technology is neutral"])

    def test_should_place_framing_text_in_framings_array_when_from_domain_model_is_called(
        self, extracted_thinking_with_all_types: ExtractedThinking
    ) -> None:
        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking_with_all_types)

        assert_that(dto.framings).is_equal_to(["Progress narrative"])

    def test_should_return_empty_claims_when_no_claims_in_positions(self) -> None:
        extracted_thinking = ExtractedThinking(
            positions=[
                Position(text="an assumption", position_type=PositionType.ASSUMPTION),
            ]
        )

        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking)

        assert_that(dto.claims).is_empty()

    def test_should_return_empty_assumptions_when_no_assumptions_in_positions(self) -> None:
        extracted_thinking = ExtractedThinking(
            positions=[
                Position(text="a claim", position_type=PositionType.CLAIM),
            ]
        )

        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking)

        assert_that(dto.assumptions).is_empty()

    def test_should_return_empty_framings_when_no_framings_in_positions(self) -> None:
        extracted_thinking = ExtractedThinking(
            positions=[
                Position(text="a claim", position_type=PositionType.CLAIM),
            ]
        )

        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking)

        assert_that(dto.framings).is_empty()

    def test_should_return_all_empty_arrays_when_positions_are_empty(self) -> None:
        extracted_thinking = ExtractedThinking(positions=[])

        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking)

        assert_that(dto.claims + dto.assumptions + dto.framings).is_empty()

    def test_should_collect_multiple_claims_when_from_domain_model_is_called(
        self, extracted_thinking_with_only_claims: ExtractedThinking
    ) -> None:
        dto = ExtractThinkingResponseDto.from_domain_model(extracted_thinking_with_only_claims)

        assert_that(dto.claims).is_equal_to(["first claim", "second claim"])
