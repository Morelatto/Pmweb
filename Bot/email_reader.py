#!/usr/bin/python

from __future__ import print_function

import getpass
import imaplib2
import os
import sys
import threading

sys.argv.append("email")
sys.argv.append("senha")

if not len(sys.argv) >= 2:
    print('* ERROR: 2 Arguments are required or just the username and password will be prompted.')
    sys.exit(1)

EMAIL_USERNAME = sys.argv[1]

if len(sys.argv) == 3:
    EMAIL_PASSWORD = sys.argv[2]
else:
    EMAIL_PASSWORD = getpass.getpass()

ServerTimeout = 29  # Mins

DEBUG = False


class Idler(threading.Thread):
    imap = imaplib2.IMAP4_SSL("imap.gmail.com")

    stopWaitingEvent = threading.Event()

    known_emails = []
    kill_now = False

    def __init__(self, username, password):

        os.system('clear')
        debug_msg('DEBUG is ENABLED')
        debug_msg('__init__() entered')

        try:
            self.imap.LOGIN(username, password)
            self.imap.SELECT("INBOX")

            typ, data = self.imap.SEARCH(None, 'ALL')
            self.known_emails = data[0].split()

            threading.Thread.__init__(self)

        except:
            print('ERROR: IMAP Issue. It could be one (or more) of the following:')
            print('- The impalib2.py file needs to be in the same directory as this file')
            print('- You\'re not connected to the internet')
            print('- Google\'s mail server(s) is/are down')
            print('- Your username and/or password is incorrect')
            print('- Invalid mailbox')
            sys.exit(1)

        debug_msg('__init__() exited')

    def run(self):
        debug_msg('run() entered')

        while not self.kill_now:
            self.wait_for_server()

        debug_msg('run() exited')

    @staticmethod
    def print_mail(title, message):
        debug_msg('print_mail() entered')

        print(' ')
        print('NEW MAIL:')
        print('--', title)
        print('--', message)
        debug_msg('print_mail() exited')
        return message

    def get_header_by_id(self, id, fields_tuple):
        debug_msg('get_header_by_id() entered')

        typ, header = self.imap.FETCH(id, '(RFC822.HEADER)')
        headerlines = header[0][1].splitlines()
        results = {}

        for field in fields_tuple:
            results[field] = ''
            for line in headerlines:
                if line.startswith(field):
                    results[field] = line

        debug_msg('get_header_by_id() exited')
        return results

    def show_new_msgs(self):
        debug_msg('show_new_msgs() entered')

        typ, data = self.imap.SEARCH(None, 'UNSEEN')

        debug_msg('data - new mail IDs:')
        debug_msg(data, 0)
        messages = []
        for id in data[0].split():
            if id not in self.known_emails:
                header_fields = self.get_header_by_id(id, ('From', 'Subject'))

                debug_msg('header_fields dict. (from showNewMailMessage()):')
                debug_msg(header_fields, 0)

                messages.append(self.print_mail(" ".join(['Mail', header_fields['From']]), "'" + header_fields['Subject'] + "'"))

                self.known_emails.append(id)

        debug_msg('show_new_msgs() exited')
        return messages

    def kill(self):
        self.kill_now = True
        self.timeout = True
        self.stopWaitingEvent.set()

    def wait_for_server(self):
        debug_msg('wait_for_server() entered')

        self.newMail = False
        self.timeout = False
        self.IDLEArgs = ''
        self.stopWaitingEvent.clear()

        def _IDLECallback(args):
            self.IDLEArgs = args
            self.stopWaitingEvent.set()

        self.imap.idle(timeout=60 * ServerTimeout, callback=_IDLECallback)

        self.stopWaitingEvent.wait()

        if not self.kill_now:

            if self.IDLEArgs[0][1][0] == 'IDLE terminated (Success)':
                typ, data = self.imap.SEARCH(None, 'UNSEEN')

                debug_msg('Data: ')
                debug_msg(data, 0)

                for id in data[0].split():
                    if id not in self.known_emails:
                        self.newMail = self.newMail or True
                    else:
                        self.timeout = True

                if data[0] == '':
                    self.timeout = True

            if self.newMail:
                debug_msg('INFO: New Mail Received')
                self.show_new_msgs()

            elif self.timeout:
                debug_msg("INFO: A Timeout Occurred")

        debug_msg("wait_for_server() exited")


def debug_msg(msg, newline=1):
    global DEBUG
    if DEBUG:
        if newline:
            print(' ')
        print(msg)


def main():
    global EMAIL_USERNAME
    global EMAIL_PASSWORD

    idler = Idler(EMAIL_USERNAME, EMAIL_PASSWORD)
    idler.start()

    print("* Waiting for mail...")
    q = ""
    while not q == "q":
        q = raw_input("Type 'q' followed by [ENTER] to quit: ")

    idler.kill()
    idler.imap.CLOSE()
    idler.imap.LOGOUT()
    sys.exit()


if __name__ == "__main__":
    main()
else:
    print("You're not supposed to import this.")
    sys.exit(1)