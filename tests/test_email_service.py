import pytest

from email_service import (
    EmailMessages,
    Messages,
    TextMessage,
    add_contacts,
    contacts_mailinglist,
    delete_contacts,
    open_or_create_email_database,
    open_or_create_email_workbook,
    render_template,
    search_contacts,
    update_contact,
    view_all_contacts,
)


# -- Fixture - create fresh in-memory database for each test --
@pytest.fixture
def db():
    """Create a fresh in-memory database for each test"""
    conn, cursor = open_or_create_email_database(":memory:")
    yield conn, cursor  # <- provides conn and cursor to each test
    conn.close()


# -- Fixture - database with sample contacts ==
@pytest.fixture
def db_with_contacts(db):
    conn, cursor = db
    add_contacts(conn, cursor, "John Doe", "+11234567890", "john.doe@example.com", "05/21/2026")
    add_contacts(conn, cursor, "Jane Doe", "+10987654321", "jane.doe@example.com", "05/21/2026")
    return conn, cursor


# -- Tests for openOrCreateEmailDatabase --
def test_database_creates_contacts_table(db):
    conn, cursor = db
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    assert "contacts" in tables


def test_database_creates_contact_answers_table(db):
    conn, cursor = db
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    assert "contact_answers" in tables


# -- Tests for add_contacts --
def test_add_contacts(db):
    conn, cursor = db
    add_contacts(conn, cursor, "John Doe", "+11234567890", "john.doe@example.com", "05/21/2026")
    cursor.execute("SELECT * FROM contacts")
    result = cursor.fetchone()
    assert result[1] == "John Doe"
    assert result[2] == "+11234567890"
    assert result[3] == "john.doe@example.com"


def test_add_multiple_contacts(db_with_contacts):
    conn, cursor = db_with_contacts
    cursor.execute("SELECT COUNT(*) FROM contacts")
    count = cursor.fetchone()[0]
    assert count == 2


# -- Tests for delete_contacts --
def test_delete_contacts(db_with_contacts):
    conn, cursor = db_with_contacts
    delete_contacts(conn, cursor, "John Doe")
    cursor.execute("SELECT * FROM contacts WHERE name = ?", ("John Doe",))


def test_delete_nonexistent_contact(db, capsys):
    conn, cursor = db
    delete_contacts(conn, cursor, "Nobody")
    captured = capsys.readouterr()
    assert "No contact found" in captured.out


def test_delete_only_correct_contact(db_with_contacts):
    conn, cursor = db_with_contacts
    delete_contacts(conn, cursor, "John Doe")
    cursor.execute("SELECT * FROM contacts WHERE name = ?", ("Jane Doe",))
    result = cursor.fetchone()
    assert result is not None  # Jane should still be there


# -- Tests for search_contacts --
def test_search_contacts_by_name(db_with_contacts, capsys):
    conn, cursor = db_with_contacts
    search_contacts(cursor, "John")
    captured = capsys.readouterr()
    assert "John" in captured.out


def test_search_contacts_not_found(db, capsys):
    conn, cursor = db
    search_contacts(cursor, "Nobody")
    captured = capsys.readouterr()
    assert "No contacts found" in captured.out


# -- Tests for contacts_mailinglist --
def test_contacts_mailinglist(db_with_contacts):
    conn, cursor = db_with_contacts
    mailing_list = contacts_mailinglist(cursor)
    assert len(mailing_list) == 2
    assert mailing_list[0]["name"] == "John Doe"
    assert mailing_list[1]["name"] == "Jane Doe"


def test_contacts_mailinglist_empty(db):
    conn, cursor = db
    mailing_list = contacts_mailinglist(cursor)
    assert mailing_list == []


def test_contacts_mailinglist_keys(db_with_contacts):
    conn, cursor = db_with_contacts
    mailing_list = contacts_mailinglist(cursor)
    assert "id" in mailing_list[0]
    assert "name" in mailing_list[0]
    assert "phone" in mailing_list[0]
    assert "email_address" in mailing_list[0]
    assert "date_added" in mailing_list[0]


# -- Tests for update_contact --
def test_update_contact(db_with_contacts):
    conn, cursor = db_with_contacts
    cursor.execute("SELECT id FROM contacts WHERE name = ?", ("John Doe",))
    contact_id = cursor.fetchone()[0]
    update_contact(conn, cursor, contact_id, "John Doe", "phone", "+19999999999")
    cursor.execute("SELECT phone FROM contacts WHERE id = ?", (contact_id,))
    result = cursor.fetchone()
    assert result[0] == "+19999999999"


def test_update_contact_invalid_field(db_with_contacts, capsys):
    conn, cursor = db_with_contacts
    cursor.execute("SELECT id FROM contacts WHERE name = ?", ("John Doe",))
    contact_id = cursor.fetchone()[0]
    update_contact(conn, cursor, contact_id, "John Doe", "invalid_field", "value")
    captured = capsys.readouterr()
    assert "Invalid field" in captured.out


# -- Test IntegrityError path in add_contacts --
def test_add_duplicate_contact(db, capsys):
    conn, cursor = db
    # Add contact twice
    add_contacts(conn, cursor, "John D", "+12468024680", "john.d@example.com", "05/21/2026")
    add_contacts(conn, cursor, "John D", "+12468024680", "john.d@example.com", "05/21/2026")
    captured = capsys.readouterr()
    assert "already exists" in captured.out  # <- IntegrityError path


# -- Test empty database paths --
def test_view_all_contacts_empty(db, capsys):
    conn, cursor = db
    view_all_contacts(cursor)
    captured = capsys.readouterr()
    assert "No contacts in database" in captured.out


def test_search_contacts_empty(db, capsys):
    con, cursor = db
    search_contacts(cursor, "John")
    captured = capsys.readouterr()
    assert "No contacts found" in captured.out


# -- Test for renderTemplate --
def test_render_template():
    html = render_template(
        "automate_email_message_template.html",
        subject="Test",
        company_name="Your Company Name",
        company_address="Your Company Address",
        recipient_name="John",
        body="Test body",
        sender_name="Your Name",
        unsubscribe_link="http://localhost:5000/unsubscribe",
        questions=[],
        items=[],
    )
    assert "Your Company Name" in html
    assert "John" in html


# -- Tests for openOrCreateEmailWorkbook --
def test_open_or_create_email_workbook(tmp_path):
    filename = str(tmp_path / "test_contacts.xlsx")
    wb = open_or_create_email_workbook(filename)
    assert wb is not None


def test_open_existing_email_workbook(tmp_path):
    filename = str(tmp_path / "test_contacts.xlsx")
    wb = open_or_create_email_workbook(filename)
    wb = open_or_create_email_workbook(filename)
    assert wb is not None


# -- Tests for Messages base class --
def test_messages_str():
    msg = Messages.__new__(Messages)
    msg.name = "John"
    msg.phone = "+11234567890"
    assert str(msg) == "John | +11234567890"


def test_messages_send_not_implemented():
    msg = Messages.__new__(Messages)
    with pytest.raises(NotImplementedError):
        msg.send()


# -- Tests for TextMessage --
def test_text_message_init():
    text = TextMessage(name="John", phone="+11234567890", body="Hello")
    assert text.name == "John"
    assert text.phone == "+11234567890"
    assert text.body == "Hello"


def test_text_message_send(capsys):
    text = TextMessage(name="John", phone="+11234567890", body="Hello")
    text.send()
    captured = capsys.readouterr()
    assert "+11234567890" in captured.out


# -- Tests for EmailMessages --
def test_email_message_init():
    email = EmailMessages(
        name="John",
        phone="+11234567890",
        email_address="john.d@example.com",
        subject="Test",
        body="Test body",
        smtp_server="smtp.gmail.com",
        smtp_port=465,
        username="sender@gmail.com",
        password="password",
    )
    assert email.name == "John"
    assert email.email_address == "john.d@example.com"
    assert email.smtp_server == "smtp.gmail.com"
