from bs4 import BeautifulSoup
import imaplib
import email
import getpass
import requests

EMAIL_ACCOUNT = "mito.mitado.mitando@gmail.com"
EMAIL_PASSWORD = getpass.getpass()
IMAP_SERVER = "imap.gmail.com"
EMAIL_FOLDER = '"[Gmail]/Todos os e-mails"'

M = imaplib.IMAP4_SSL(IMAP_SERVER)


def process_message(msg):
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_payload(decode=1)
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.findAll(src=True):
                src = str(link["src"])
                if src.endswith(".php"):
                    print(requests.get(src), src)


def process_mailbox():
    response, emails = M.search(None, "ALL")
    if response != 'OK':
        print("No messages found.")
        return

    for email_id in emails[0].split():
        rv, data = M.fetch(email_id, '(RFC822)')
        if rv != 'OK':
            print("Error getting message", email_id)
            return

        msg = email.message_from_bytes(data[0][1])
        process_message(msg)


def login():
    try:
        M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print("Login Failed.")


def open_mailbox(mailbox):
    rv, data = M.select(mailbox)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox()
        M.close()
    else:
        print("Invalid folder.")
    M.logout()


def main():
    login()
    open_mailbox(EMAIL_FOLDER)


main()
