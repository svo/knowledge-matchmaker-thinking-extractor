from pydantic import BaseModel


class ExtractRequest(BaseModel):
    draft: str


class ExtractResponse(BaseModel):
    claims: list[str]
    assumptions: list[str]
    framings: list[str]
