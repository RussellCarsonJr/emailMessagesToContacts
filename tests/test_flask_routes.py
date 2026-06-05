import os
import sqlite3
import tempfile

import pytest

import app as flask_app
from app import app


# -- Fixture - creates Flask test client --
@pytest.fixture
def client():
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    app.template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Override FILENAME with temp database:
    flask_app.FILENAME = db_path

    with app.test_client() as client:
        yield client

    # Cleanup temp database after tests:
    os.close(db_fd)
    os.unlink(db_path)


# -- Tests for /contacts route --
def test_contacts_page_loads(client):
    response = client.get("/contacts")
    assert response.status_code == 200


def test_contacts_page_contains_company_name(client):
    response = client.get("/contacts")
    assert b"Your Company Name" in response.data


def test_contacts_page_contains_questions(client):
    response = client.get("/contacts")
    assert b"How satisfied are you" in response.data


# -- Tests for /submit_answers route --
def test_submit_answers(client):
    response = client.post(
        "/submit_answers",
        data={
            "recipient_name": "Johm Doe",
            "answer_1": "Very satisfied",
            "answer_2": "Yes",
            "answer_3": "More classes",
        },
    )
    assert response.status_code == 200


def test_submit_answers_shows_confirmation(client):
    response = client.post(
        "/submit_answers",
        data={
            "recipient_name": "John Doe",
            "answer_1": "Very Satisfied",
            "answer_2": "Yes",
            "answer_3": "More classes",
        },
    )
    assert b"Thank you for your feedback" in response.data


# -- Tests for /unsubscribe route --
def test_unsubscribe_page_loads(client):
    response = client.get("/unsubscribe")
    assert response.status_code == 200


def test_unsubscribe_page_contains_form(client):
    response = client.get("/unsubscribe")
    assert b"Enter your full name" in response.data


def test_unsubscribe_post(client):
    response = client.post("/unsubscribe", data={"recipient_name": "John Doe"})
    assert response.status_code == 200


# -- Test empty fields in submit_answers --
def test_submit_answers_empty_fields(client):
    response = client.post(
        "/submit_answers",
        data={"recipient_name": "", "answer_1": "", "answer_2": "", "answer_3": ""},  # <- empty name  # <- empty answer
    )
    assert response.status_code == 200


# -- Test unsubscribe with nonexistent contact --
def test_unsubscribe_nonexistent_contact(client, capsys):
    response = client.post("/unsubscribe", data={"recipient_name": "Nobody"})
    assert response.status_code == 200
    assert b"has been deleted" in response.data


# -- Test database error handling --
def test_submit_answers_database_error(client, monkeypatch):
    # monkeypatch replaces openOrCreateEmailDatabase with a version that raises an error
    def mock_db_error(filename):
        raise sqlite3.OperationalError("Database is locked")

    monkeypatch.setattr("app.open_or_create_email_database", mock_db_error)

    response = client.post(
        "/submit_answers",
        data={"recipient_name": "John D", "answer_1": "Great", "answer_2": "Yes", "answer_3": "Nothing"},
    )
    assert response.status_code == 503  # <- service unavailable
