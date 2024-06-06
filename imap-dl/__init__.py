import imaplib
import json
import email
from os import chdir, mkdir
from os.path import exists
from socket import gaierror
from sys import exit

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

# Login to mailbox
mailbox = imaplib.IMAP4_SSL(HOST)
mailbox.login(USER, PASS)

# Retrieve all mail from inbox
mailbox.select("Inbox")
_, data = mailbox.search(None, "ALL")


# Function for mail retrieval
def retrieve_mail(mailbox: imaplib.IMAP4, upper: int, lower:int):
    print(upper, lower)
    _, data = mailbox.fetch(f"{lower}:{upper}", "(RFC822)")
    for mail in data:
        # Skip if item is not proper mail
        if not isinstance(mail, tuple):
            continue

        # Parse mail
        mail_parsed = email.message_from_bytes(mail[1])
        date = email.utils.parsedate_to_datetime(mail_parsed["Date"]).isoformat()
        subject = "".join(char for char in mail_parsed["Subject"] if char not in "\/:*?<>|")[0:50]

        # Save to file
        filename = f"{date} ---- {subject}.eml"
        with open(filename, "wb") as file:
            file.write(mail[1])
        print("I: Saved - %s" % filename)


if __name__ == "__main__":
    try:
        # Retrieve individual mail
        chdir(DIRNAME)
        mail_count = len(data[0].split())
        while True:
            if mail_count > 100:
                retrieve_mail(mailbox, mail_count, mail_count := mail_count - 100)
                mail_count -= 1
            else:
                retrieve_mail(mailbox, mail_count, 1)
                break
            

    # Handle net error or bad hostname
    except gaierror or NameError as e:
        print(
            "E: Connection could not be made - check internet and host information in config.json"
        )

    # Handle incorrect authentication
    except imaplib.IMAP4.error as e:
        print("E: Authentication error - check login details in config.json")

    # End connection to IMAP server if no errors occurred or terminated using Ctrl+C
    except KeyboardInterrupt:
        print("\nW: Keyboard interrupt detected - exiting")
        mailbox.close()
        mailbox.logout()
        exit()
    else:
        mailbox.close()
        mailbox.logout()
        exit()
