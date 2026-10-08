from datetime import datetime

from pydantic import BaseModel, Field


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

     class Config:
          from_attributes = True