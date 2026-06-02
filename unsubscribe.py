#! /usr/bin/env python3.10
# unsubscribeLink.py - deletes searched contact

from email_service import delete_contacts, open_or_create_email_database


def unsubscribe_contact(name):
    conn, cursor = open_or_create_email_database
    name = input("Enter your full name to unsubscribe: ")
    delete_contacts(conn, cursor, name)


if __name__ == "__main__":
    pass
