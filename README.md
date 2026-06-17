# emailMessagesToContacts

A Flask web application for sending bulk HTML emails to contacts
stored in a SQLite database.

## Features
- Send bulk HTML emails with attachments
- Manage contacts in SQLite database
- Collect feedback via web form
- Unsubscribe functionality

## Setup
1. Clone the repository
2. Install dependencies:
   pipenv install
3. Set environment variable:
   export EMAIL_PASSWORD="your_gmail_app_password"
4. Run the Flask app:
   pipenv run python app.py

## Testing
pipenv run pytest -v

## Documentation
https://RussellCarsonJr.github.io/emailMessagesToContacts/
