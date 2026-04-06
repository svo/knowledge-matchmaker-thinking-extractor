from __future__ import annotations

from pydantic import BaseModel, Field

from knowledge_matchmaker_thinking_extractor.domain.model.position import Position


class ExtractedThinking(BaseModel):
    positions: list[Position] = Field(default_factory=list)
