from unittest.mock import MagicMock, patch

from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.position import PositionType
from knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor import (
    ClaudeThinkingExtractor,
)


class TestClaudeThinkingExtractor:
    @patch("knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor.anthropic")
    def test_should_return_extracted_thinking_with_positions(self, mock_anthropic):
        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.input = {
            "positions": [
                {"text": "AI will transform education", "position_type": "CLAIM"},
                {"text": "Technology is neutral", "position_type": "ASSUMPTION"},
            ]
        }
        mock_response = MagicMock()
        mock_response.content = [tool_use_block]
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response

        extractor = ClaudeThinkingExtractor()
        result = extractor.extract(Draft(text="AI will transform education"))

        assert_that(result.positions).is_length(2)

    @patch("knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor.anthropic")
    def test_should_extract_claim_position_type(self, mock_anthropic):
        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.input = {
            "positions": [
                {"text": "AI will transform education", "position_type": "CLAIM"},
            ]
        }
        mock_response = MagicMock()
        mock_response.content = [tool_use_block]
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response

        extractor = ClaudeThinkingExtractor()
        result = extractor.extract(Draft(text="AI will transform education"))

        assert_that(result.positions[0].position_type).is_equal_to(PositionType.CLAIM)

    @patch("knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor.anthropic")
    def test_should_extract_position_text(self, mock_anthropic):
        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.input = {
            "positions": [
                {"text": "AI will transform education", "position_type": "CLAIM"},
            ]
        }
        mock_response = MagicMock()
        mock_response.content = [tool_use_block]
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response

        extractor = ClaudeThinkingExtractor()
        result = extractor.extract(Draft(text="AI will transform education"))

        assert_that(result.positions[0].text).is_equal_to("AI will transform education")

    @patch("knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor.anthropic")
    def test_should_return_empty_positions_when_none_found(self, mock_anthropic):
        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.input = {"positions": []}
        mock_response = MagicMock()
        mock_response.content = [tool_use_block]
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response

        extractor = ClaudeThinkingExtractor()
        result = extractor.extract(Draft(text="nothing meaningful"))

        assert_that(result.positions).is_empty()
