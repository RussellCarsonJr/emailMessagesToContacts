# emailMessagesToContacts -Claude Code Configuration

## Project Overview
A Flask web application for sending bulk HTML emails and iMessages
to contacts stored in a SQLite database. Built for Learning Dreams,
a business based in Burton, MI.

## Tech Stack
- Python 3.10
- Flask (web framework)
- SQLite (database with WAL mode for concurrency)
- Jinja2 (HTML email templates)
- Pipenv (virtual environment and dependency management)
- pytest (testing framework)
- Black (code formatter)
- Ruff (linter)
- mypy (type checker)
- pdoc (documentation generator)

## Project Structure


emailMessagesToContacts/email_service.py←email classes and database functions
app.py←Flask web routes unsubscribe.py←Excel workbook unsubscribe function
imessage_apple_text_messages.py←iMessage database functions sendimessage.py←
sends iMessages (Mac only) messages.py←legacy file (keep for reference) Pipfile←project
dependencies Pipfile.lock←locked dependency versions pyproject.toml←tool
configuration .env←environment variables (not committed) .gitignore←git ignore rules
README.md←project documentation templates/
automate_email_message_template.html← browser feedback form
automate_email_message_template4.html ←email version of form
submit_answers_template.html←feedback confimation
unsubscribe_email_message_template.html←email_unsubscribe
unsubscribe_text_imessage_template.html←text unsubscribe error_template.html←error
page tests/init.py test_email_service.py←tests for email_service.py test_flask_routes.py←
tests for Flask routes docs/ ←auto-generated API documentation


## Commands

### Development
'''bash
# Activate virtual environment:
pipenv shell

# Run Flask app locally:
pipenv run python app.py

# Send iMessages (Mac only):
python3.10 sendimessage.py
'''

### Code Quality
'''bash
# Format code:
pipenv run black .

# Lint code:
pipenv run ruff check .

# Auto-fix lint errors:
pipenv run ruff check --fix

# Type check:
pipenv run mypy email_service.py


# Format HTML templates:
pipenv run djlint templates/
'''

### Testing
'''bash
# Run all tests:
pipenv run pytest -v

# Run with coverage report:
pipenv run pytest --cov=email_service --cov=app --cov-report=term-missing -v

# Run specific test file:
pipenv run pytest tests/test_email_service.py -v

# Run specific test:
pipenv run pytest tests/test_email_service.py::test_add_contacts -v


### Documentation
'''bash
# Generate API docs:
pipenv run pdoc email_service.py app.py --output-dir docs

# View docs locally:
open docs/email_service.html
'''

### Git Workflow
'''bash
# Daily workflow:
pipenv run black .
pipenv run ruff check .
pipenv run pytest -v
git add .
cit commit -m "type: description"
git push
'''

### Commit Message Types

feat:  new feature
fix:  bug fix
test:  adding tests
docs:  documentation
refactor:code restructure
style:  formatting
config: configuration changes
chore:  maintenance


## Environment Variables
Required in '.env' (never commit this file):


EMAIL_PASSWORD=your_gmail_app_password SENDER_EMAIL=your@gmail.com
DB_FILENAME =/path/to/automate_email_message_contacts.db ATTACHMENT_PATH=/
path/to/attachment.jpg TEXT_DB_FILENAME=/path/to/text_imessage_contacts.db
TEXT_UNSUBSCRIBE_LINK=https://yoursite.pythonanywhere.com/text_unsubscribe
COMPANY_NAME=Your Business Name COMPANY_ADDRESS=Your Business Address
SENDER_NAME=Your Name


## Data Schema

### automate_email_message_contacts.db
'''sql
-- Email contacts table
CREATE TABLE contacts (
    id			INTEGER PRIMARY KEY AUTOINCREMENT,
    name		TEXT NOT NULL,
    phone		TEXT NOT NULL,
    email_adderss       TEXT NOT NULL UNIQUE,
    date_added		DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Feedback answers table
CREATE TABLE contact_answers (
    id 		INTEGER PRIMARY KEY AUTOINCREMENT,
    name	TEXT NOT NULL,
    answer_1	TEXT NOT NULL,
    answer_2	TEXT NOT NULL,
    answer_3 	TEXT NOT NULL
);
'''

### text_imessage_contacts.db
'''sql
-- iMessage contacts table
CREATE TABLE text_contacts (
    id 			INTEGER PRIMARY KEY AUTOINCREMENT,
    name 		TEXT NOT NULL,
    phone		TEXT NOT NULL,
    email_address	TEXT NOT NULL UNIQUE,
    date_added		DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Text feedback answers table
CREATE TABLE text_contact_answers (
    id		INTEGER PRIMARY KEY AUTOINCREMENT,
    name 	TEXT NOT NULL,
    answer_1	TEXT NOT NULL,
    answer_2 	TEXT NOT NULL,
    answer_3	TEXT NOT NULL
);
'''

## Flask Routes

GET/contacts	→displys feedback form
POST/submit_answers →savesanswers to database
GET/unsubscribe    →display email unsubscribe form
POST/unsubscribe    →deletescontact from email database
GET/text_unsubscribe →displaystext unsubscribe form
POST/text_unsubscribe →deletescontact from text database


## Key Classes (email_service.py)

Messages    →baseclass for all message types
EmailMessages    →sendsHTML emails via SMTP_SSL
AutomateEmailMessage →sendsbulk emails to mailing list
TextMessage    →sendsiMessages(Mac only)


## Key Functions (email_service.py)

render_template()	→rendersJinja2 HTML template
contacts_mailinglist()    →returns all contacts as list of dicts
open_or_create_email_database() →createsor opens SQLite database
add_contacts()    →add ssingle contact to database
add_multiple_contacts()    →add list of contacts to database
delete_contacts()	→deletescontact by exact name match
view_all_contacts()	→displaysall contacts in terminal
search_contacts()    →searchescontacts by name/phone/email
update_contact()    →updatesa specific contact field
close_database()    →closesdatabase connection
open_or_create_email_workbook() →createsor opens Excel workbook
write_header()    →writesstyled header to Excel sheet 	


## Deployment (PythonAnywhere)

URL:https://RussellCarsonJr.pythonanywhere.com WSGI file:/var/www/
russellcarsonjr_pythonanywhere_com_wsgi.py Files:/home/RussellCarsonJr/Python
version: 3.9(PythonAnywhere virtual environment)


## Important Notes
- sendimessage.py ONLY runs on Mac - uses osascript to control Messages app
- Always use pipenv run prefix for all commands
- Never commit .env file - contains sensitive credentials
- Database files (*.db) are in .gitignore - not committed to Git
- Coverage threshold is set to 67% in project.toml
- PythonAnywhere uses Python 3.9, local development uses Python 3.10
- WAL mode enabled on all SQLite databases for concurrency support
- Email forms in templates do not save directly must go through Flask routes


