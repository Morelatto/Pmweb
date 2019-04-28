# -*- coding: utf-8 -*-

import json
import os
import sys
import urllib

from scrapy import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.spiders.init import InitSpider
from scrapy.utils.project import get_project_settings
from utilities.email_checker import EmailChecker


def get_list(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(base_path, "..", "..", file_name))
    with open("{0}_list.txt".format(file_path), 'r') as file_:
        list_ = file_.read().splitlines()
    return list_


class ProofSpider(InitSpider):
    name = "proof"

    def __init__(self, info, *a, **kw):
        super(ProofSpider, self).__init__(*a, **kw)

        try:
            account, password, pod = info.split(':')
        except ValueError:
            sys.exit("Invalid arguments. Usage: scrapy reports -a info=account:password:pod")

        self.username = account
        self.password = password

        self.base_url = "https://interact{0}.responsys.net/".format(pod)
        self.settings = get_project_settings()

        self.email_checker = EmailChecker(self.logger, self.settings.get("IMAP_EMAIL_ADDRESS"),
                                          self.settings.get("IMAP_EMAIL_PASSWORD"))

        try:
            self.proof_list = get_list("emails_proof")
            campaign_list = get_list("campaign")
        except IOError:
            sys.exit("Could not open files emails_proof_list.txt and campaign_list.txt.")

        self.start_urls = [self.base_url + "interact/folder/getCampaignId?campaignName={0}".format(campaign) for campaign in campaign_list]
        

    def init_request(self):
        return Request(
            url=self.base_url + "authentication/login/LoginPage",
            callback=self.login
        )

    def login(self, response):
        form_tag = Selector(text=response.body).xpath("//form[@id='loginForm']")
        if form_tag:
            form_data = {
                "hScreenWidth": "",
                "hScreenHeight": "",
                "UserName": self.username,
                "Password": self.password
            }

            return FormRequest.from_response(
                response,
                formxpath="//form[@id='loginForm']",
                formdata=form_data,
                callback=self.check_login
            )
        else:
            self.logger.error("Could not find login form element. Possibly due to maintenance.")
            return

    def check_login(self, response):
        if "Login Failed" in response.body:
            self.logger.error("Incorrect username or password.")
            return
        else:
            if "First time login from this computer" in response.body or \
                            "A verification code was sent to your email associated with your account" in response.body:
                return Request(
                    url=self.base_url + "authentication/login/LoginEmailCodeAction",
                    callback=self.verification_code
                )
            else:
                if "accountName" in response.body:
                    return Request(
                        url=self.base_url + "suite/c#!home",
                        callback=self.check_verification_code
                    )
                else:
                    self.logger.error("Login failed")
                    self.logger.info(response.body)
                    return

    def verification_code(self, response):
        if "A verification code was sent to your email associated with your account" in response.body:
            self.logger.info("Waiting for verification code...")
            code = self.email_checker.wait_for_emails(self.username)
            self.logger.info(code)
            if not code:
                self.logger.warning("Enter the verification code: ")
                code = raw_input()

            return FormRequest(
                url=self.base_url + "authentication/login/LoginEnterCodeAction",
                formdata={
                    "VerificationCode": code,
                    "ckBoxValidDays": "on"
                },
                callback=self.check_verification_code
            )
        else:
            self.logger.error("Access to authentication code page failed.")
            return

    def check_verification_code(self, response):
        self.email_checker.logout()
        if "Activation failed" in response.body:
            self.logger.error("Authentication code failed")
            return
        else:
            self.logger.info("Login successful")
            return self.initialized()

    def parse(self, response):
        campaign_id = response.body.strip()
        campaign_name = urllib.unquote(response.url[response.url.index('=') + 1:]).decode("utf8")

        if not campaign_id:
            self.logger.warning("Campaign %s does not exist.", campaign_name)
            return

        form_data = {
            "campaignId": campaign_id,
            "isProfileList": True,
            "proofToAddress": ",".join(self.proof_list),
            "isHtmlFormatSelected": True,
            "limit": 1
        }

        yield Request(
            url=self.base_url + "emd/c/campaigndesigner/email/request/prooflaunch",
            method='POST',
            body=json.dumps(form_data),
            headers={
                "Content-Type": "application/json",
                "Referer": self.base_url + "emd/c/campaigndesigner/framework/page/launch?campaignId=" + campaign_id,
                "X-Requested-With": "XMLHttpRequest"
            },
            meta={
                "handle_httpstatus_list": [500, 400],
                "campaign_name": campaign_name
            },
            dont_filter=True,
            callback=self.proof_launch
        )

    def proof_launch(self, response):
        status = str(response.status)
        if status == "200":
            self.logger.info("[SUCCESS] Proof launch for campaign %s succeeded.", response.request.meta["campaign_name"])
        elif status == "400":
            self.logger.info("[INVALID] Campaign %s with errors.", response.request.meta["campaign_name"])
        else:
            self.logger.info("[FAIL] Proof launch for campaign %s failed.", response.request.meta["campaign_name"])
        return
