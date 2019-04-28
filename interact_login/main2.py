#!/usr/bin/env python
# -*- coding: utf-8 -*-

from interact_login.utilities.db_code import CodeDatabase
from interact_login.utilities.email_checker_t import EmailChecker
from interact_login.spiders.login import LoginSpider

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor, defer


configure_logging()
settings = get_project_settings()

db_con = CodeDatabase()
idler = EmailChecker(settings.get("IMAP_EMAIL_ADDRESS", ""), settings.get("IMAP_EMAIL_PASSWORD", ""), db_con)
idler.start()

runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(LoginSpider, account="", password="", pod="", db_con=db_con)
    yield runner.crawl(LoginSpider, account="", password="", pod="", db_con=db_con)
    reactor.stop()

crawl()

reactor.run()
idler.exit()
db_con.close_db()
