# -*- coding: utf-8 -*-

import email
import imaplib2
import re
import sys
import threading

# TODO Log


class EmailChecker(threading.Thread):
    imap = imaplib2.IMAP4_SSL("imap.gmail.com")
    stop_waiting_event = threading.Event()
    kill_now = False
    server_timeout = 29

    def __init__(self, username, password, db_code_con=None):
        self.known_emails = []
        self.timeout = self.new_mail = False
        self.IDLE_args = ''
        self.accounts_list = []
        self.db_code_con = db_code_con

        try:
            self.imap.LOGIN(username, password)
            self.imap.SELECT("INBOX")

            typ, data = self.imap.SEARCH(None, "ALL")
            self.known_emails = data[0].split()

            threading.Thread.__init__(self)
        except:
            sys.exit("[IMAP] Error.")

    def run(self):
        while not self.kill_now:
            self.wait_for_server()

    def get_email_content(self, email_id):
        typ, data = self.imap.FETCH(email_id, "(RFC822)")
        for response_part in data:
            if isinstance(response_part, tuple):
                raw_email = email.message_from_string(response_part[1])
                if email.utils.parseaddr(raw_email["From"])[0] == "donotreply@responsys.net":
                    email_message = raw_email.get_payload()

                    account = re.search(r"Dear (.+):", email_message, re.IGNORECASE)
                    if account:
                        code = re.search(r"(\d{6})", email_message)
                        if code:
                            self.imap.STORE(email_id, "+FLAGS", "\\Seen")
                            return account.group(1), code.group()

    def show_new_mail_messages(self, data):
        if data:
            for email_id in data[0].split():
                if email_id not in self.known_emails:
                    account, code = self.get_email_content(email_id)
                    if account and code:
                        if self.db_code_con:
                            self.save_code(account, code)
                        else:
                            print "{0} - {1}".format(account, code)
                    self.known_emails.append(email_id)

    def kill(self):
        self.kill_now = True
        self.timeout = True
        self.stop_waiting_event.set()

    def wait_for_server(self):
        self.stop_waiting_event.clear()

        def _IDLE_callback(args):
            self.IDLE_args = args
            self.stop_waiting_event.set()

        self.imap.idle(timeout=60 * self.server_timeout, callback=_IDLE_callback)

        self.stop_waiting_event.wait()

        if not self.kill_now:
            data = None
            if self.IDLE_args[0][1][0] == "IDLE terminated (Success)":
                typ, data = self.imap.SEARCH(None, "UNSEEN")

                for email_id in data[0].split():
                    if email_id not in self.known_emails:
                        self.new_mail = self.new_mail or True
                    else:
                        self.timeout = True

                if data[0] == '':
                    self.timeout = True

            if self.new_mail:
                self.show_new_mail_messages(data)

            elif self.timeout:
                pass

    def save_code(self, account, code):
        self.db_code_con.insert_code(account, code)

    def exit(self):
        self.kill()
        self.imap.CLOSE()
        self.imap.LOGOUT()
