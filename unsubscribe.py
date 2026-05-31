#! /usr/bin/env python3.10
# unsubscribeLink.py - deletes searched contact

import openpyxl
from openpyxl import Workbook
import os

# -- Constants --------------------------------------------------
FILENAME                = "/home/RussellCarsonJr/messageContacts.xlsx"



from openOrCreateMessageWorkbook import(
    openOrCreateWorkbook,
    searchContact,
    deleteContacts
)

def unsubscribeContact(filename, name):
    wb = openOrCreateWorkbook(filename)
    searchContact(wb, name)
    deleteContacts(wb, filename, name)
    wb.save(filename)

if __name__ == "__main__":
    FILENAME = "messageContacts.xlsx"
    name = input("Enter name to search for: ")
    unsubscribeContact(FILENAME, name)


