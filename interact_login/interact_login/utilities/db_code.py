# -*- coding: utf-8 -*-

import sqlite3

from datetime import datetime


class CodeDatabase(object):
    def __init__(self):
        self.con = sqlite3.connect(".interact_codes.db", check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_codes_table()

    def create_codes_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Codes("
                         "id INTEGER PRIMARY KEY, account TEXT UNIQUE, code TEXT, created_date DATE)")

    def insert_code(self, account, code):
        if account and code:
            self.cur.execute("INSERT OR REPLACE INTO Codes(account, code, created_date) VALUES(?, ?, ?)",
                             (account, code, str(datetime.now()),))

    def select_code(self, account):
        if account:
            self.cur.execute("SELECT code FROM Codes WHERE account = ?", (account,))
            code = self.cur.fetchall()
            return code[0][0] if code else None

    def drop_codes_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Codes")
        self.con.commit()

    def close_db(self):
        self.drop_codes_table()
        self.con.close()
