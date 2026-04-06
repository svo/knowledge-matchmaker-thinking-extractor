from unittest.mock import Mock

from assertpy import assert_that
import anthropic

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.infrastructure.llm.claude_thinking_extractor import ClaudeThinkingExtractor


def _make_mock_client(claims: list, assumptions: list, framings: list) -> Mock:
    tool_use_block = Mock()
    tool_use_block.type = "tool_use"
    tool_use_block.input = {"claims": claims, "assumptions": assumptions, "framings": framings}

    message = Mock()
    message.content = [tool_use_block]

    client = Mock(spec=anthropic.Anthropic)
    client.messages = Mock()
    client.messages.create = Mock(return_value=message)
    return client


class TestClaudeThinkingExtractor:
    def test_should_return_claims_when_extraction_succeeds(self) -> None:
        client = _make_mock_client(["claim1"], [], [])
        extractor = ClaudeThinkingExtractor(client=client)
        draft = Draft(text="test")

        result = extractor.extract(draft)

        assert_that(result.claims).contains("claim1")

    def test_should_return_assumptions_when_extraction_succeeds(self) -> None:
        client = _make_mock_client([], ["assumption1"], [])
        extractor = ClaudeThinkingExtractor(client=client)
        draft = Draft(text="test")

        result = extractor.extract(draft)

        assert_that(result.assumptions).contains("assumption1")

    def test_should_return_framings_when_extraction_succeeds(self) -> None:
        client = _make_mock_client([], [], ["framing1"])
        extractor = ClaudeThinkingExtractor(client=client)
        draft = Draft(text="test")

        result = extractor.extract(draft)

        assert_that(result.framings).contains("framing1")

    def test_should_call_claude_api_when_extracting(self) -> None:
        client = _make_mock_client([], [], [])
        extractor = ClaudeThinkingExtractor(client=client)
        draft = Draft(text="test")

        extractor.extract(draft)

        assert_that(client.messages.create.call_count).is_equal_to(1)
