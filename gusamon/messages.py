from pydantic import BaseModel, Field


class Message(BaseModel):
    is_epic: bool = Field(...)
    payload: str = Field(...)
