from pydantic import BaseModel


class ExtractedThinking(BaseModel):
    claims: list[str]
    assumptions: list[str]
    framings: list[str]
