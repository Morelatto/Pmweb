from time import sleep

import email
import re
import imaplib
import sys


class EmailChecker:
    def __init__(self, logger, account, password):
        self.logger = logger
        self.M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        try:
            self.M.login(account, password)
            self.clear_unread()
        except imaplib.IMAP4.error:
            sys.exit("[IMAP] Login to {0} failed.".format(account))

    def clear_unread(self):
        self.M.list()
        self.M.select('INBOX')
        code, messages = self.M.search(None, '(UNSEEN)')
        if code == 'OK':
            for message_id in messages[0].split():
                self.M.store(message_id, '+FLAGS', '\\Seen')

    def wait_for_emails(self, interact_account):
        i = 5
        while True:
            if i < 25:
                self.M.list()
                self.M.select('INBOX')
                code, messages = self.M.search(None, '(UNSEEN)')
                if code == 'OK':
                    for message_id in messages[0].split():
                        typ, data = self.M.fetch(message_id, '(RFC822)')
                        for response_part in data:
                            if isinstance(response_part, tuple):
                                raw_email = email.message_from_string(response_part[1])
                                if email.utils.parseaddr(raw_email['From'])[0] == 'donotreply@responsys.net':
                                    self.M.store(message_id, '+FLAGS', '\\Seen')
                                    email_message = raw_email.get_payload()

                                    account = re.search(r'Dear (.+):', email_message, re.IGNORECASE)
                                    if account:
                                        if account.group(1) == interact_account:
                                            code = re.search(r'(\d{6})', email_message)
                                            if code:
                                                return code.group()
                                            else:
                                                self.logger.warning('[IMAP] No code match.')
                                    else:
                                        self.logger.warning('[IMAP] No account match.')
                                    return
                sleep(i)
                i += 5
            else:
                self.logger.warning('[IMAP] Failed to retrieve code after trying 5 times')
                return

    def logout(self):
        self.M.close()
        self.M.logout()
