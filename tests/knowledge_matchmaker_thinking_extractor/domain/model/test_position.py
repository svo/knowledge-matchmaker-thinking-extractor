from __future__ import annotations

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType


class TestPosition:
    def test_should_have_text(self) -> None:
        position = Position(text="some claim", position_type=PositionType.CLAIM)

        assert_that(position.text).is_equal_to("some claim")

    def test_should_have_position_type(self) -> None:
        position = Position(text="some claim", position_type=PositionType.CLAIM)

        assert_that(position.position_type).is_equal_to(PositionType.CLAIM)

    def test_should_accept_claim_type(self) -> None:
        position = Position(text="explicit assertion", position_type=PositionType.CLAIM)

        assert_that(position.position_type).is_equal_to(PositionType.CLAIM)

    def test_should_accept_assumption_type(self) -> None:
        position = Position(text="unstated premise", position_type=PositionType.ASSUMPTION)

        assert_that(position.position_type).is_equal_to(PositionType.ASSUMPTION)

    def test_should_accept_framing_type(self) -> None:
        position = Position(text="conceptual lens", position_type=PositionType.FRAMING)

        assert_that(position.position_type).is_equal_to(PositionType.FRAMING)
