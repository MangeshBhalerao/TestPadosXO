from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import NoteCreate, NoteResponse, NoteUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(
     title="Notes API",
     description="A simple Notes API built with FastAPI and SQLite",
     version="1.0.0"
)


@app.post(
     "/notes",
     response_model=NoteResponse,
     status_code=status.HTTP_201_CREATED
)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
     return crud.create_note(db, note)

@app.get(
     "/notes",
     response_model=list[NoteResponse]
)
def list_notes(
     search: str | None = Query(default=None),
     db: Session = Depends(get_db)
):
     return crud.get_notes(db, search)


@app.get(
     "/notes/{note_id}",
     response_model=NoteResponse
)
def get_note(note_id: int, db: Session = Depends(get_db)):
     note = crud.get_note(db, note_id)

     if note is None:
          raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Note not found"
          )

     return note


@app.put(
     "/notes/{note_id}",
     response_model=NoteResponse
)
def update_note(
     note_id: int,
     note: NoteUpdate,
     db: Session = Depends(get_db)
):
     updated_note = crud.update_note(db, note_id, note)

     if updated_note is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Note not found"
          )

     return updated_note


@app.delete(
     "/notes/{note_id}"
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
     deleted_note = crud.delete_note(db, note_id)

     if deleted_note is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Note not found"
          )

     return {
          "message": "Note deleted successfully",
          "note_id": note_id
     }