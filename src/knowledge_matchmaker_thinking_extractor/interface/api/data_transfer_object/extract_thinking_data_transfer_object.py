from __future__ import annotations

from typing import Any

from pydantic import BaseModel

_CLAIM = "CLAIM"
_ASSUMPTION = "ASSUMPTION"
_FRAMING = "FRAMING"


class ExtractThinkingRequestDto(BaseModel):
    draft: str


class ExtractThinkingResponseDto(BaseModel):
    claims: list[str]
    assumptions: list[str]
    framings: list[str]

    @staticmethod
    def _texts_by_type(positions: Any, position_type: str) -> list[str]:
        return [p.text for p in positions if p.position_type.value == position_type]

    @classmethod
    def from_domain_model(cls, extracted_thinking: Any) -> ExtractThinkingResponseDto:
        positions = extracted_thinking.positions
        return cls(
            claims=cls._texts_by_type(positions, _CLAIM),
            assumptions=cls._texts_by_type(positions, _ASSUMPTION),
            framings=cls._texts_by_type(positions, _FRAMING),
        )
