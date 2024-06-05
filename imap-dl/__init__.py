import imaplib
import json
from os import chdir
from socket import gaierror
from sys import exit

# Retrieve host and credentials from config
chdir(__file__.removesuffix("/__init__.py"))
with open("config.json") as file:
    config: dict = json.load(file)
    HOST = config["host"]
    USER = config["email"]
    PASS = config["password"]

try:
    # Login to mailbox
    mailbox = imaplib.IMAP4_SSL(HOST)
    mailbox.login(USER, PASS)

    # Retrieve all mail from inbox
    mailbox.select("Inbox")
    typ, data = mailbox.search(None, "ALL")

    # Retrieve individual mail
    count = 1
    for num in data[0].split():
        typ, data = mailbox.fetch(num, "(RFC822)")
        with open("mail.eml", "wb") as file:
            file.write(data[0][1])
        print("Mail %i received" % count)
        count += 1

# Handle net error or bad hostname
except gaierror or NameError as e:
    print("E: Connection could not be made - probably because of no internet or bad config")

# Handle incorrect authentication
except imaplib.IMAP4.error as e:
    print("E: Authentication error - ")

# End connection to IMAP server if no error occurred
else:
    mailbox.close()
    mailbox.logout()
