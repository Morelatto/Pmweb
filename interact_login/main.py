#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import CrawlerRunner, logger
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from interact_login.spiders.login import LoginSpider
from interact_login.utilities.db_code import CodeDatabase
from interact_login.utilities.email_checker_t import EmailChecker


def _load_csv(file_name):
    accounts_info = list()
    try:
        with open(file_name, "rb") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            seen_accounts = set()

            for row in csv_reader:
                if row[0] in seen_accounts:
                    continue

                seen_accounts.add(row[0])
                accounts_info.append(row)
    except IOError:
        logger.error("Could not read '{0}'.".format(file_name))
        sys.exit(0)
    return accounts_info


def _get_cookies(host, db_name, user, password):
    db = MySQLdb.connect(host=host, db=db_name, user=user, passwd=password, cursorclass=MySQLdb.cursors.DictCursor)
    cur = db.cursor()

    cur.execute("SELECT account, name, value, domain, path, path_specified, secure, discard, expires FROM Cookie")

    cookie_dicts = {cookie.get("account"): {cookie.get("name"): cookie.get("value")} for cookie in cur.fetchall()}

    db.close()
    return cookie_dicts


def main():
    # TODO Check if main page is available

    settings = get_project_settings()
    configure_logging(settings)

    accounts = _load_csv(settings.get("ACCOUNTS_FILE"))
    cookies = _get_cookies(settings.get("MYSQL_HOST"), settings.get("MYSQL_DBNAME"), settings.get("MYSQL_USER"),
                           settings.get("MYSQL_PASSWD"))
    db_code_con = CodeDatabase()
    idler = EmailChecker(settings.get("IMAP_EMAIL_ADDRESS"), settings.get("IMAP_EMAIL_PASSWORD"), db_code_con)

    idler.start()
    runner = CrawlerRunner(settings)

    start = 0
    end = 9

    while end < len(cookies):
        run(accounts[start:end], runner, db_code_con, cookies)
        start = end + 1
        end += 10

    _exit(idler, db_code_con)


def run(accounts, runner, db_code_con, cookies):
    for account in accounts:
        runner.crawl(LoginSpider, account=account[0], password=account[1], pod=account[2], db_code_con=db_code_con,
                     login_cookie=cookies.get(account[0], {}))

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


def _exit(idler, db_code_con):
    idler.exit()
    db_code_con.close_db()


if __name__ == "__main__":
    main()
