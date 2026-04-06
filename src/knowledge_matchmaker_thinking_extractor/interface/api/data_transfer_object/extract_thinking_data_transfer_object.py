from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ExtractThinkingRequestDto(BaseModel):
    text: str


class PositionDto(BaseModel):
    text: str
    position_type: str

    @classmethod
    def from_domain_model(cls, position: Any) -> PositionDto:
        return cls(text=position.text, position_type=position.position_type.value)


class ExtractThinkingResponseDto(BaseModel):
    positions: list[PositionDto]

    @classmethod
    def from_domain_model(cls, extracted_thinking: Any) -> ExtractThinkingResponseDto:
        return cls(positions=[PositionDto.from_domain_model(p) for p in extracted_thinking.positions])
