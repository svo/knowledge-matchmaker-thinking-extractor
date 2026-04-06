import anthropic

from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.port.thinking_extractor_port import ThinkingExtractorPort


class ClaudeThinkingExtractor(ThinkingExtractorPort):
    def __init__(self, client: anthropic.Anthropic) -> None:
        self._client = client

    def extract(self, draft: Draft) -> ExtractedThinking:
        message = self._client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=[self._extraction_tool()],
            tool_choice={"type": "tool", "name": "extract_thinking"},
            messages=[{"role": "user", "content": self._prompt(draft.text)}],
        )
        return self._parse_response(message)

    def _extraction_tool(self) -> dict:
        return {
            "name": "extract_thinking",
            "description": "Extract the epistemic structure of the user's draft.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "claims": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Explicit assertions the author is making.",
                    },
                    "assumptions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Unstated premises the argument rests on.",
                    },
                    "framings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Conceptual vocabulary or lenses the author is working within.",
                    },
                },
                "required": ["claims", "assumptions", "framings"],
            },
        }

    def _prompt(self, text: str) -> str:
        return (
            "Extract the epistemic structure from the following draft. "
            "Identify: (1) explicit claims the author asserts, "
            "(2) implicit assumptions their argument rests on, "
            "(3) conceptual framings or vocabulary they operate within.\n\n"
            f"Draft:\n{text}"
        )

    def _parse_response(self, message: anthropic.types.Message) -> ExtractedThinking:
        tool_use = next(block for block in message.content if block.type == "tool_use")
        data = tool_use.input
        return ExtractedThinking(
            claims=data["claims"],
            assumptions=data["assumptions"],
            framings=data["framings"],
        )
