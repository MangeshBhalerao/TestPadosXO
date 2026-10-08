from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
     SQLALCHEMY_DATABASE_URL,
     connect_args={"check_same_thread": False},
     poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
     autocommit=False,
     autoflush=False,
     bind=engine
)


Base.metadata.create_all(bind=engine)


def override_get_db():
     db = TestingSessionLocal()

     try:
          yield db
     finally:
          db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function():
     Base.metadata.drop_all(bind=engine)
     Base.metadata.create_all(bind=engine)


def test_create_note_success():
     response = client.post(
          "/notes",
          json={
               "title": "Shopping list",
               "content": "Buy milk"
          }
     )

     assert response.status_code == 201

     data = response.json()

     assert data["title"] == "Shopping list"
     assert data["content"] == "Buy milk"
     assert "id" in data
     assert "created_at" in data


def test_list_notes():
     client.post(
          "/notes",
          json={
               "title": "First note",
               "content": "First content"
          }
     )

     client.post(
          "/notes",
          json={
               "title": "Second note",
               "content": "Second content"
          }
     )

     response = client.get("/notes")

     assert response.status_code == 200

     data = response.json()

     assert len(data) == 2
     assert data[0]["title"] == "Second note"


def test_get_note_by_id():
     create_response = client.post(
          "/notes",
          json={
               "title": "Test note",
               "content": "Test content"
          }
     )

     note_id = create_response.json()["id"]

     response = client.get(f"/notes/{note_id}")

     assert response.status_code == 200

     data = response.json()

     assert data["id"] == note_id
     assert data["title"] == "Test note"


def test_update_note():
     create_response = client.post(
          "/notes",
          json={
               "title": "Old title",
               "content": "Old content"
          }
     )

     note_id = create_response.json()["id"]

     response = client.put(
          f"/notes/{note_id}",
          json={
               "title": "Updated title",
               "content": "Updated content"
          }
     )

     assert response.status_code == 200

     data = response.json()

     assert data["title"] == "Updated title"
     assert data["content"] == "Updated content"


def test_delete_note():
     create_response = client.post(
          "/notes",
          json={
               "title": "Delete me",
               "content": "This will be deleted"
          }
     )

     note_id = create_response.json()["id"]

     response = client.delete(f"/notes/{note_id}")

     assert response.status_code == 200

     data = response.json()

     assert data["message"] == "Note deleted successfully"

     get_response = client.get(f"/notes/{note_id}")

     assert get_response.status_code == 404


def test_invalid_note_returns_404():
     response = client.get("/notes/99999")

     assert response.status_code == 404
     assert response.json()["detail"] == "Note not found"


def test_validation_error_for_empty_title():
     response = client.post(
          "/notes",
          json={
               "title": "",
               "content": "Some content"
          }
     )

     assert response.status_code == 422