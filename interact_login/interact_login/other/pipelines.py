# -*- coding: utf-8 -*-

import sqlite3


class SQLiteCookiePipeline(object):
    def __init__(self):
        self.con = sqlite3.connect("interact_cookies.db")
        self.cur = self.con.cursor()
        self.create_cookies_table()

    def close_spider(self, spider):
        self.con.close()

    def create_cookies_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Cookie(
                            id INTEGER PRIMARY KEY,
                            account TEXT UNIQUE,
                            name TEXT,
                            value TEXT,
                            domain TEXT,
                            path_specified BOOLEAN,
                            path TEXT,
                            secure BOOLEAN,
                            discard TEXT,
                            expires DATE,
                            crawled_date DATE)''')

    def process_item(self, item, account):
        self.store_in_db(item, account)
        return item

    def store_in_db(self, item, account):
        if account and item:
            self.cur.execute('''INSERT OR REPLACE INTO Cookie(
                                account,
                                name,
                                value,
                                domain,
                                path_specified,
                                path,
                                secure,
                                discard,
                                expires,
                                crawled_date)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (account,
                              item.get("name", ''),
                              item.get("value", ''),
                              item.get("domain", ''),
                              item.get("path_specified", False),
                              item.get("path", ''),
                              item.get("secure", False),
                              item.get("discard", 0),
                              item.get("expires", ''),
                              item.get("crawled_date", ''),
                              ))
            self.con.commit()
