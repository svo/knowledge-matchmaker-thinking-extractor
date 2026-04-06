from __future__ import annotations

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft


class TestDraft:
    def test_should_have_text(self) -> None:
        draft = Draft(text="some text")

        assert_that(draft.text).is_equal_to("some text")
