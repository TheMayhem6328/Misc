import imaplib
import json
import email
from os import chdir, mkdir
from os.path import exists
from socket import gaierror

# Resolve directories and create as needed
DIRNAME = "emails"
chdir(__file__.removesuffix("/__init__.py"))
if not exists(DIRNAME):
    mkdir(DIRNAME)

# Retrieve host and credentials from config.json
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
    chdir(DIRNAME)
    for num in data[0].split():
        typ, data = mailbox.fetch(num, "(RFC822)")
        mail = email.message_from_bytes(data[0][1])
        date = email.utils.parsedate_to_datetime(mail["Date"]).isoformat()
        subject = mail["Subject"]
        filename = f"{str(num, encoding='ASCII').zfill(5)} ---- {date} ---- {subject}.eml"
        with open(filename, "wb") as file:
            file.write(data[0][1])
        print("I: Saved - %s" % filename)

# Handle net error or bad hostname
except gaierror or NameError as e:
    print("E: Connection could not be made - check internet and host information in config.json")

# Handle incorrect authentication
except imaplib.IMAP4.error as e:
    print("E: Authentication error - check login details in config.json")

# End connection to IMAP server if no errors occurred or terminated using Ctrl+C
except KeyboardInterrupt:
    print("W: Keyboard interrupt detected - exiting")
    mailbox.close()
    mailbox.logout()
else:
    mailbox.close()
    mailbox.logout()
