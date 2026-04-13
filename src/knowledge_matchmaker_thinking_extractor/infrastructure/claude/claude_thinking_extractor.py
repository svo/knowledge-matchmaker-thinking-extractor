from __future__ import annotations

import os
from typing import Any, Dict, List, cast

import anthropic
from anthropic.types import ToolChoiceToolParam, ToolParam

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType
from knowledge_matchmaker_thinking_extractor.domain.service.thinking_extractor import ThinkingExtractor

_EXTRACT_POSITIONS_TOOL: ToolParam = {
    "name": "extract_positions",
    "description": "Extract epistemic positions from a draft text",
    "input_schema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text of the position",
                        },
                        "position_type": {
                            "type": "string",
                            "enum": ["CLAIM", "ASSUMPTION", "FRAMING"],
                            "description": "The type of epistemic position",
                        },
                    },
                    "required": ["text", "position_type"],
                },
            }
        },
        "required": ["positions"],
    },
}

_SYSTEM_PROMPT = (
    "You are an expert at identifying the epistemic structure of written arguments. "
    "Given a draft text, identify all epistemic positions: "
    "CLAIM positions are explicit assertions the author is making; "
    "ASSUMPTION positions are unstated premises the argument rests on; "
    "FRAMING positions are the conceptual lenses or vocabulary the author works within."
)


class ClaudeThinkingExtractor(ThinkingExtractor):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self._model = "claude-haiku-4-5-20251001"

    def extract(self, draft: Draft) -> ExtractedThinking:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            tools=[_EXTRACT_POSITIONS_TOOL],
            tool_choice=ToolChoiceToolParam(type="tool", name="extract_positions"),
            messages=[{"role": "user", "content": draft.text}],
        )

        tool_use_block = next(block for block in response.content if block.type == "tool_use")
        tool_input = cast(Dict[str, Any], tool_use_block.input)
        raw_positions: List[Dict[str, str]] = tool_input["positions"]

        positions = [Position(text=p["text"], position_type=PositionType(p["position_type"])) for p in raw_positions]

        return ExtractedThinking(positions=positions)
