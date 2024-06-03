import imaplib
import json

# Retrieve host and credentials from config
with open("config.json") as file:
    config: dict = json.load(file)
    HOST = config["host"]
    USER = config["email"]
    PASS = config["password"]

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
    print("Mail %i received" % count)
    count += 1

# End connection to IMAP server
mailbox.close()
mailbox.logout()
