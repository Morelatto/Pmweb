# -*- coding: utf-8 -*-

from twisted.enterprise import adbapi

from interact_login.items import CookieItem, AccountItem


class MySQLPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_args = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **db_args)
        return cls(db_pool)

    def close_spider(self, spider):
        self.db_pool.close()

    def process_item(self, item, spider):
        if isinstance(item, CookieItem):
            d = self.db_pool.runInteraction(self._insert_cookie, item, spider)
            d.addErrback(self._handle_cookie_error, item, spider)
            d.addBoth(lambda _: item)
            return d
        elif isinstance(item, AccountItem):
            d = self.db_pool.runInteraction(self._insert_account, item, spider)
            d.addErrback(self._handle_account_error, item, spider)
            d.addBoth(lambda _: item)
            return d

    @staticmethod
    def _insert_cookie(conn, item, spider):
        params = (
            item.get("account"), item.get("name"), item.get("value"), item.get("domain"), item.get("path_specified"),
            item.get("path"), item.get("secure"), item.get("discard"), item.get("expires"), item.get("crawled_date"),
        )
        conn.execute("REPLACE INTO Cookie "
                     "(account, name, value, domain, path_specified, path, secure, discard, expires, crawled_date)"
                     " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", params)
        spider.logger.info(
            "Cookie for {0} stored in db: {1} - {2}".format(item.get("account"), item.get("name"), item.get("value")))

    @staticmethod
    def _insert_account(conn, item, spider):
        conn.execute("INSERT INTO Account (account_name, account_status, crawled_date) VALUE (%s, %s, %s)",
                     (item.get("account"), item.get("status"), item.get("crawled_date"),))
        spider.logger.info("Status for {0} stored in db.".format(item.get("account")))

    @staticmethod
    def _handle_cookie_error(failure, item, spider):
        spider.logger.debug("Failed to store {0} cookie in db: {1} - {2}".format(item.get("account"), item.get("name"),
                                                                                 item.get("value")))
        spider.logger.error(failure)

    @staticmethod
    def _handle_account_error(failure, item, spider):
        spider.logger.debug("Failed to store status for {0}".format(item.get("account")))
        spider.logger.error(failure)
