from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking


class TestExtractedThinking:
    def test_should_store_claims_when_created(self) -> None:
        thinking = ExtractedThinking(claims=["claim1"], assumptions=[], framings=[])

        assert_that(thinking.claims).contains("claim1")

    def test_should_store_assumptions_when_created(self) -> None:
        thinking = ExtractedThinking(claims=[], assumptions=["assumption1"], framings=[])

        assert_that(thinking.assumptions).contains("assumption1")

    def test_should_store_framings_when_created(self) -> None:
        thinking = ExtractedThinking(claims=[], assumptions=[], framings=["framing1"])

        assert_that(thinking.framings).contains("framing1")
