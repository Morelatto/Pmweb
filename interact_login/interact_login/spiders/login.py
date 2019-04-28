# -*- coding: utf-8 -*-

import time
from datetime import datetime

from scrapy.http import FormRequest, Request
from scrapy.spiders import CrawlSpider
from twisted.internet import reactor
from twisted.internet.threads import deferToThreadPool

from interact_login.items import AccountItem


class LoginSpider(CrawlSpider):
    name = "login"

    def __init__(self, *a, **kw):
        super(LoginSpider, self).__init__(*a, **kw)
        self.cookies = []

        self.account = kw.get("account")
        self.password = kw.get("password")
        self.base_url = "https://interact{0}.responsys.net/".format(kw.get("pod"))
        self.db_code_con = kw.get("db_code_con")
        self.login_cookie = kw.get("login_cookie")

    def start_requests(self):
        return [FormRequest(
                    url=self.base_url + "authentication/login/LoginAction",
                    formdata=dict(UserName=self.account, Password=self.password, hScreenWidth="", hScreenHeight=""),
                    headers=dict(Referer=self.base_url + "authentication/login/LoginPage"),
                    cookies=self.login_cookie,
                    callback=self.check_login
                )]

    def check_login(self, response):
        if "Login failed" in response.body:
            self.logger.error("Incorrect username, password or pod for {0}.".format(self.account))
            status = "Incorrect username, password or pod."
        elif "accountName" in response.body:
            return Request(
                url=self.base_url + "interact/jsp/jindex.jsp",
                callback=self.check_verification_code
            )
        elif "First time login from this computer" in response.body:
            return Request(
                url=self.base_url + "authentication/login/LoginEmailCodeAction",
                callback=self.verification_code
            )
        elif "A verification code was sent to your email associated with your account" in response.body:
            self.logger.warning("Code was already requested for {0}. Requesting another one.".format(self.account))
            return Request(
                url=self.base_url + "authentication/login/LoginEmailCodeAction?clickhere=true",
                callback=self.verification_code
            )
        elif "Password Expired" in response.body:
            self.logger.error("Password expired for {0}.".format(self.account))
            status = "Password expired."
        elif "User has been locked" in response.body:
            self.logger.error("User locked for {0}.".format(self.account))
            status = "User locked."
        else:
            self.logger.error("Login failed for {0}.".format(self.account))
            status = "Login failed. Unknown."
        return Request(
            url=self.base_url,
            callback=self.parse_status,
            meta=dict(status=status)
        )

    def verification_code(self, response):
        if "A verification code was sent to your email associated with your account" in response.body:
            return deferToThreadPool(reactor, reactor.getThreadPool(), self.wait_for_verification_code)

        elif "User has been locked" in response.body:
            self.logger.error("User was locked for {0}.".format(self.account))
            status = "User has been locked."
        else:
            self.logger.error("Access to authentication code page failed for {0}.".format(self.account))
            status = "Access to authentication code page failed. Unknown."
        return Request(
            url=self.base_url,
            callback=self.parse_status,
            meta=dict(status=status)
        )

    def wait_for_verification_code(self):
        self.logger.info("Waiting 10 seconds for verification code of {0}...".format(self.account))
        time.sleep(10)

        code = self.db_code_con.select_code(self.account)

        if not code:
            self.logger.info("Waiting 20 more seconds for verification code of {0}...".format(self.account))
            time.sleep(20)
            code = self.db_code_con.select_code(self.account)

        if code:
            self.logger.info("{0} - {1}".format(self.account, code))
            return FormRequest(
                url=self.base_url + "authentication/login/LoginEnterCodeAction",
                formdata=dict(VerificationCode=str(code), ckBoxValidDays="on"),
                callback=self.check_verification_code
            )
        else:
            self.logger.error("Failed to retrieve code after 30 seconds for {0}.".format(self.account))
            return Request(
                url=self.base_url,
                callback=self.parse_status,
                meta=dict(status="Failed to retrieve verification code.")
            )

    def check_verification_code(self, response):
        if "Activation failed" in response.body:
            self.logger.error("Authentication code failed for {0}".format(self.account))
            status = "Activation failed."
        elif "Password Expired" in response.body:
            self.logger.error("Logged in but password expired for {0}.".format(self.account))
            status = "Password expired."
        else:
            self.logger.info("Login successful for {0}.".format(self.account))
            return Request(
                url=self.base_url + "interact/jsp/jindex.jsp",
                callback=self.parse_item
            )
        return Request(
            url=self.base_url,
            callback=self.parse_status,
            meta=dict(status=status)
        )

    def parse_item(self, response):
        for cookie in self.cookies:
            yield cookie

        yield Request(
            url=self.base_url + "interact/jsp/jindex.jsp",
            callback=self.logout
        )

    def logout(self, response):
        self.logger.info("Logging out {0}.".format(self.account))

        return Request(
            url=self.base_url + "interact/login/Logout?/login",
            callback=self.parse_status,
            meta=dict(status="Success.")
        )

    def parse_status(self, response):
        account_item = AccountItem()
        account_item["account"] = self.account
        account_item["status"] = response.meta.get("status")
        account_item["crawled_date"] = str(datetime.now())

        yield account_item
