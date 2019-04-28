import imaplib
import email
import getpass

EMAIL_ACCOUNT = ""
EMAIL_PASSWORD = getpass.getpass()
IMAP_SERVER = "imap.gmail.com"
EMAIL_FOLDER = '"[Gmail]/Todos os e-mails"'

M = imaplib.IMAP4_SSL(IMAP_SERVER)


def create_email_text(msg, subject):
    import time
    file = open(time.strftime("%Y%m%d-%H%M%S")+".txt", 'wb')
    file.write(msg)
    file.close()
    print("===")


def process_message(msg):
    subject = str(email.header.make_header(email.header.decode_header(msg['Subject'])))
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            content = part.get_payload(decode=True)
            create_email_text(content, subject + ".txt")
        else:
            continue


def process_mailbox():
    response, emails = M.search(None, '(TO "suporte@pmweb.com.br" NOT FROM "suporte@pmweb.com.br")')
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

if __name__ == "__main__":
    main()
