# -*- coding: utf-8 -*-

BOT_NAME = "interact_login"

SPIDER_MODULES = ["interact_login.spiders"]
NEWSPIDER_MODULE = "interact_login.spiders"

# LOG_LEVEL = "INFO"
LOG_STDOUT = True
# LOG_FILE = "log.txt"

ROBOTSTXT_OBEY = False

RETRY_TIMES = 1

DOWNLOAD_TIMEOUT = 30

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"

TELNETCONSOLE_ENABLED = False

DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": None,
    "interact_login.middlewares.cookies.PersistentCookiesMiddleware": 701
}

ITEM_PIPELINES = {
    "interact_login.pipelines.MySQLPipeline": 300
}

IMAP_EMAIL_ADDRESS = ""
IMAP_EMAIL_PASSWORD = ""

MYSQL_HOST = ""
MYSQL_DBNAME = ""
MYSQL_USER = ""
MYSQL_PASSWD = ""

ACCOUNTS_FILE = ""

'''
IMAP_EMAIL_ADDRESS = ""
IMAP_EMAIL_PASSWORD = ""

MYSQL_HOST = ""
MYSQL_DBNAME = ""
MYSQL_USER = ""
MYSQL_PASSWD = ""

ACCOUNTS_FILE = ""
'''
