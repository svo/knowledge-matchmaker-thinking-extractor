from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class PositionType(str, Enum):
    CLAIM = "CLAIM"
    ASSUMPTION = "ASSUMPTION"
    FRAMING = "FRAMING"


class Position(BaseModel):
    text: str
    position_type: PositionType
