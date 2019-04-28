# -*- coding: utf-8 -*-

from datetime import datetime

from scrapy.downloadermiddlewares.cookies import CookiesMiddleware

from interact_login.items import CookieItem


class PersistentCookiesMiddleware(CookiesMiddleware):
    def __init__(self, debug=False):
        super(PersistentCookiesMiddleware, self).__init__(debug)

    def process_response(self, request, response, spider):
        if request.meta.get("dont_merge_cookies", False):
            return response

        cookie_jar_key = request.meta.get("cookiejar")
        jar = self.jars[cookie_jar_key]
        jar.extract_cookies(response, request)

        self._process_cookies(response, request, spider, jar)
        self._debug_set_cookie(response, spider)

        return response

    def _process_cookies(self, response, request, spider, jar):
        if response:
            cookies = jar.make_cookies(response, request)
            for cookie in cookies:
                cookie_name = getattr(cookie, "name", '')
                if cookie_name.startswith("rida_"):
                    cookie_item = self._generate_each_cookie(cookie, spider.account)
                    spider.cookies.append(cookie_item)

    @staticmethod
    def _generate_each_cookie(cookie, account):
        if cookie:
            cookie_item = CookieItem()
            cookie_item["account"] = account
            cookie_item["name"] = getattr(cookie, "name", '')
            cookie_item["value"] = getattr(cookie, "value", '')
            cookie_item["domain"] = getattr(cookie, "domain", '')
            cookie_item["path"] = getattr(cookie, "path", '')
            cookie_item["path_specified"] = getattr(cookie, "path_specified", '')
            cookie_item["secure"] = getattr(cookie, "secure", '')
            cookie_item["discard"] = getattr(cookie, "discard", '')

            if hasattr(cookie, "expires"):
                if cookie.expires:
                    cookie_item["expires"] = str(datetime.fromtimestamp(float(cookie.expires)))
            cookie_item["crawled_date"] = str(datetime.now())

            return cookie_item
