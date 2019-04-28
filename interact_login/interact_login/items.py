# -*- coding: utf-8 -*-

from scrapy import Field, Item


class CookieItem(Item):
    account = Field()
    name = Field()
    value = Field()
    domain = Field()
    path = Field()
    path_specified = Field()
    secure = Field()
    discard = Field()
    expires = Field()
    crawled_date = Field()


class AccountItem(Item):
    account = Field()
    status = Field()
    crawled_date = Field()
