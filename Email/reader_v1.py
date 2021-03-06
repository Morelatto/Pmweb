import sys
import imaplib
import email
import email.header
import datetime
import re

EMAIL_ACCOUNT = "mito.mitado.mitando@gmail.com"
EMAIL_PASSWORD = ""

EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        # hdr = email.header.make_header(email.header.decode_header(msg['Subject']))

        msg.as_string()
        print("=================================================")
        print(msg)
        print("=================================================")

        # msgstring = str(msg)

        # xx = re.search('src\s*=\s*"(.+?)"', msgstring)
        #
        # if xx:
        #     print(xx.group(0))  # → xyz@xyz.com
        # else:
        #     print("no")

        # subject = str(hdr)
        # print('Message %s: %s' % (num, subject))
        # print('Raw Date:', msg['Date'])
        # # Now convert to local date-time
        # date_tuple = email.utils.parsedate_tz(msg['Date'])
        # if date_tuple:
        #     local_date = datetime.datetime.fromtimestamp(
        #         email.utils.mktime_tz(date_tuple))
        #     print("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))


M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()
