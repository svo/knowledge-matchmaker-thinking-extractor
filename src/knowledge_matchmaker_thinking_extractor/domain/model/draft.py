from pydantic import BaseModel


class Draft(BaseModel):
    text: str
