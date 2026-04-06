from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft


class TestDraft:
    def test_should_store_text_when_draft_is_created(self) -> None:
        draft = Draft(text="some argument")

        assert_that(draft.text).is_equal_to("some argument")
