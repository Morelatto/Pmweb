from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
import time
import ImageGrab


def start_bot():
    browser = webdriver.Chrome(executable_path="chromedriver.exe")
    return browser


class Bot(object):

    def __init__(self, user, password, account, pod, running=True):
        self.user = user
        self.password = password
        self.account = account
        self.pod = pod
        if not running:
            self.browser = start_bot()

    def log_in(self):
        self.browser.get("https://interact" + self.pod + ".responsys.net/authentication/login/LoginPage")

        username = self.browser.find_element_by_id("txtUserName")
        password = self.browser.find_element_by_id("txtPassword")

        username.send_keys(self.user)
        password.send_keys(self.password)

        login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']")
        login_attempt.submit()

    def login_code(self):
        self.browser.get("https://interact" + self.pod + ".responsys.net/authentication/login/LoginEmailCodeAction")
        # try:
        #     element_present = EC.presence_of_element_located((By.ID, 'button-1031'))
        #     WebDriverWait(self.browser, 3).until(element_present)
        # except TimeoutException:
        #     print "Timed out waiting for page to load"
        # time.sleep(25)
        # try:
        #     info = email_reader.get_code()
        #     textfield = self.browser.find_element_by_id("textfield-1029-inputEl")
        #     ok = False
        #     for account_info in info:
        #         if account_info[1] == self.user.lower():
        #             textfield.send_keys(account_info[0])
        #             button = self.browser.find_element_by_id("button-1031")
        #             button.click()
        #             ok = True
        #             break
        # except:
        #     ok = False
        # if not ok:
        raw_input("Press enter for " + self.account)

    def attempt_creation_user(self):
        self.browser.get("https://interact" + self.pod + ".responsys.net/interact/account/UserNew")

        error_message = ""

        try:
            error_message = self.browser.find_element_by_id('ui.account.campaignManagement.exceedLimit')
        except:
            error_message = ""
        finally:
            if error_message != "":
                self.browser.get("https://interact" + self.pod + ".responsys.net/interact/newaccount/UserList")
                time.sleep(1)
                im = ImageGrab.grab()
                im.save(self.account + ".png")
                self.browser.get("https://interact" + self.pod + ".responsys.net/interact/login/Logout?/login")
                return False
            else:
                return True

    def fill_fields(self):
        login_name = self.browser.find_element_by_name("UserName")
        email = self.browser.find_element_by_name("EMail")
        display_name = self.browser.find_element_by_name("DisplayName")

        login_name.send_keys("pmweb_api_" + self.account.lower())
        email.send_keys("op@pmweb.com.br")
        display_name.send_keys("Pmweb API - " + self.account.title())

        select = self.browser.find_element_by_id('authUIRoleCategorySelector')
        for option in select.find_elements_by_tag_name('option'):
            if option.text == ' Legacy Restrictions ':
                option.click()
                break

        all_inputs = self.browser.find_elements_by_tag_name("input")
        for input in all_inputs:
            if input.get_attribute("value") == "CannotAccessUIWebServicesAccessOnly":
                input.click()

    def create_user(self):
        uicommoncreate = self.browser.find_element_by_id("ui.common.create")
        uicommoncreate.click()

    def logout(self):
        self.browser.get("https://interact" + self.pod + ".responsys.net/interact/login/Logout?/login")
