#! /usr/bin/env python3.10
# automateEmailMessageFlask.py - sends bulk html email messages

import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request

from email_service import (
    delete_contacts,
    open_or_create_email_database,
)

load_dotenv()

app = Flask(__name__)

FILENAME = os.environ.get("DB_FILENAME") or "automate_email_message_contacts.db"
<<<<<<< HEAD
VAR_COMPANY_NAME = os.environ.get("COMPANY_NAME")
VAR_COMPANY_ADDRESS = os.environ.get("COMPANY_ADDRESS")
VAR_SENDER_NAME = os.environ.get("SENDER_NAME")
VAR_SUBJECT = os.environ.get("DEFAULT_SUBJECT")
=======
VAR_COMPANY_NAME = os.environ.get("COMPANY_NAME", "Your Company Name")
VAR_COMPANY_ADDRESS = os.environ.get("COMPANY_ADDRESS", "Your Company Address")
VAR_SENDER_NAME = os.environ.get("SENDER_NAME", "Your Name")
VAR_SUBJECT = os.environ.get("DEFAULT_SUBJECT", "Your Subject")
>>>>>>> 8284f4ddaad42239baf7103fd9ff2a845d2c8abe

@app.route("/contacts")
def contacts():
    conn, cursor = open_or_create_email_database(FILENAME)
    conn.close()

    # for i in range(len(mailing_list)):
    return render_template(
        "automate_email_message_template.html",
        subject=VAR_SUBJECT,
        company_name=VAR_COMPANY_NAME,
<<<<<<< HEAD
        company_address="Your Company Address",
=======
        company_address=VAR_COMPANY_ADDRESS,
>>>>>>> 8284f4ddaad42239baf7103fd9ff2a845d2c8abe
        recipient_name="Valued Customer",
        body="We appreciate your continued support.",
        sender_name=VAR_SENDER_NAME,
        unsubscribe_link="https://RussellCarsonJr.pythonanywhere.com/unsubscribe",
        questions=[
            "How satisfied are you with our service?",
            "Would you recommend us to a friend?",
            "How can we improve?",
        ],
    )


@app.route("/submit_answers", methods=["POST"])
def submit_answers():

    name = request.form.get("recipient_name")
    answer1 = request.form.get("answer_1")
    answer2 = request.form.get("answer_2")
    answer3 = request.form.get("answer_3")
    try:
        # Save to database
        conn, cursor = open_or_create_email_database(FILENAME)
        cursor.execute(
            """
            INSERT INTO contact_answers (name, answer_1, answer_2, answer_3)
            VALUES (?, ?, ?, ?)
        """,
            (name, answer1, answer2, answer3),
        )
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return (
            render_template("error_template.html", message="We're experiencing high traffic. Please try again."),
            503,
        )  # <- 503 = service temporarily unavailable

    return render_template(
        "submit_answers_template.html",
        company_name=VAR_COMPANY_NAME,
        company_address=VAR_COMPANY_ADDRESS,
        recipient_name=name,
        body="Thank you for your feedback!",
        sender_name=VAR_SENDER_NAME,
        answer_1=answer1,
        answer_2=answer2,
        answer_3=answer3,
        unsubscribe_link="https://RussellCarsonJr.pythonanywhere.com/unsubscribe",
    )


@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    name = ""
    body = "Please enter your name to unsubscribe."

    if request.method == "POST":
        name = request.form.get("recipient_name")
        print(f"Attempting to delete: {name}")
        conn, cursor = open_or_create_email_database(FILENAME)
        delete_contacts(conn, cursor, name)
        conn.close()
        body = f"Your name: {name} has been deleted from 'Your Business' Name' contact list."

    return render_template(
        "unsubscribe_email_message_template.html",
        subject="Unsubscribe",
        company_name=VAR_COMPANY_NAME,
        company_address=VAR_COMPANY_ADDRESS,
        recipient_name=name,
        body=body,
        sender_name=VAR_SENDER_NAME,
        unsubscribe_link="https://RussellCarsonJr.pythonanywhere.com/unsubscribe",
        unsubscribe_page=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
