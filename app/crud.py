from sqlalchemy.orm import Session

from .models import Note
from .schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate):
     db_note = Note(
          title=note.title,
          content=note.content
     )

     db.add(db_note)
     db.commit()
     db.refresh(db_note)

     return db_note


def get_notes(db: Session, search: str | None = None):
     query = db.query(Note)

     if search:
          query = query.filter(Note.title.ilike(f"%{search}%"))

     return query.order_by(Note.created_at.desc()).all()


def get_note(db: Session, note_id: int):
     return db.query(Note).filter(Note.id == note_id).first()


def update_note(db: Session, note_id: int, note: NoteUpdate):
     db_note = get_note(db, note_id)

     if db_note is None:
          return None

     db_note.title = note.title
     db_note.content = note.content

     db.commit()
     db.refresh(db_note)

     return db_note


def delete_note(db: Session, note_id: int):
     db_note = get_note(db, note_id)

     if db_note is None:
          return None

     db.delete(db_note)
     db.commit()

     return db_note