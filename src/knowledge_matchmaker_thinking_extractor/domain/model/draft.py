from __future__ import annotations

from pydantic import BaseModel


class Draft(BaseModel):
    text: str
