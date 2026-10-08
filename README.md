# Notes API

A simple RESTful Notes API built with FastAPI, SQLAlchemy and SQLite.

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest

## Features

- Create notes
- List notes
- Get a single note
- Update notes
- Delete notes
- Input validation
- 404 handling
- Search notes by title
- Automated tests

## Project Structure

```text
notes-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── tests/
│   └── test_notes.py
├── requirements.txt
├── README.md
└── .gitignore