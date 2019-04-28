# -*- coding: utf-8 -*-

BOT_NAME = "proof_crawler"

SPIDER_MODULES = ["proof_crawler.spiders"]
NEWSPIDER_MODULE = "proof_crawler.spiders"

LOG_DATEFORMAT = "%d-%m-%Y %H:%M:%S"

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

CONCURRENT_REQUESTS = 1

ROBOTSTXT_OBEY = False

TELNETCONSOLE_ENABLED = False

IMAP_EMAIL_ADDRESS = ""
IMAP_EMAIL_PASSWORD = ""

RETRY_HTTP_CODES = [502, 503, 504, 408]
