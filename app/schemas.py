from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
     title: str = Field(..., min_length=1, max_length=100)
     content: str = Field(..., min_length=1, max_length=1000)


class NoteUpdate(BaseModel):
     title: str = Field(..., min_length=1, max_length=100)
     content: str = Field(..., min_length=1, max_length=1000)


class NoteResponse(BaseModel):
     id: int
     title: str
     content: str
     created_at: datetime

     model_config = ConfigDict(from_attributes=True)