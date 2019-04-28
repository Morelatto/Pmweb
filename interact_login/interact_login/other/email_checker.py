# -*- coding: utf-8 -*-

import email
import imaplib
import re
import time


class EmailChecker:
    logged = False

    def __init__(self, account, password):
        self.M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        try:
            self.M.LOGIN(account, password)
            self.clear_unread()
            self.logged = True
        except imaplib.IMAP4.error:
            print "[IMAP] Login to '{0}' failed.".format(account)

    def clear_unread(self):
        self.M.LIST()
        self.M.SELECT("INBOX")
        code, messages = self.M.search(None, "(UNSEEN)")
        if code == "OK":
            for message_id in messages[0].split():
                self.M.store(message_id, "+FLAGS", "\\Seen")

    def wait_for_mail(self, interact_account):
        i = 7
        known_emails = list()
        while True:
            time.sleep(i)
            if i < 19:
                self.M.LIST()
                self.M.SELECT("INBOX")
                code, messages = self.M.SEARCH(None, "(UNSEEN)")
                if code == "OK":
                    for message_id in messages[0].split():
                        if message_id not in known_emails:
                            typ, data = self.M.FETCH(message_id, "(RFC822)")
                            for response_part in data:
                                if isinstance(response_part, tuple):
                                    raw_email = email.message_from_string(response_part[1])
                                    if email.utils.parseaddr(raw_email["From"])[0] == "donotreply@responsys.net":
                                        email_message = raw_email.get_payload()

                                        account = re.search(r"Dear (.+):", email_message, re.IGNORECASE)
                                        if account:
                                            if account.group(1) == interact_account:
                                                code = re.search(r"(\d{6})", email_message)
                                                if code:
                                                    self.M.STORE(message_id, "+FLAGS", "\\Seen")
                                                    return code.group()
                                                else:
                                                    print "[IMAP] No code match on message {0}.".format(message_id)
                                        else:
                                            print "[IMAP] No account match on message {0}.".format(message_id)
                    known_emails += messages[0].split()
                i += 3
            else:
                print "[IMAP] Failed to retrieve code for '{0}' after waiting a minute.".format(interact_account)
                return

    def logout(self):
        try:
            self.M.CLOSE()
            self.M.LOGOUT()
        except imaplib.IMAP4.error:
            pass
