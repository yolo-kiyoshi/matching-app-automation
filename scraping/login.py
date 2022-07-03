import os
import time

import pyotp
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

SELENIUM_URL = os.environ["SELENIUM_URL"]
OTP_CODE = os.environ["OTP_CODE"]
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]


def login_fb(driver, email, password):

    driver.find_element_by_css_selector("#email").send_keys(email)
    driver.find_element_by_css_selector("#pass").send_keys(password)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input").click()


def auth_otp(driver, otp_code):
    # ワンタイムパスワード
    # https://pypi.org/project/pyotp/
    totp = pyotp.TOTP(otp_code)
    driver.find_element_by_css_selector("#approvals_code").send_keys(totp.now())
    driver.find_element_by_css_selector("#checkpointSubmitButton").click()


def set_browser(driver):
    # ブラウザ未保存
    driver.find_elements_by_name("name_action_selected")[1].click()
    driver.find_element_by_css_selector("#checkpointSubmitButton").click()


def login():

    driver = webdriver.Remote(command_executor=SELENIUM_URL, desired_capabilities=DesiredCapabilities.FIREFOX.copy())
    driver.get("https://pairs.lv")
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/main/div/div[1]/div[2]/button[1]").click()

    # https://qiita.com/QUANON/items/285ad7157619b0da5c67
    # 新規ウィンドウを認識するまで待機
    WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])

    login_fb(driver, EMAIL, PASSWORD)
    time.sleep(5)
    # 画面遷移、ワンタイムパスワード設定画面
    driver.switch_to.window(driver.window_handles[1])
    auth_otp(driver, OTP_CODE)
    time.sleep(5)
    # ブラウザ未保存
    set_browser(driver)
    # ホーム画面に遷移
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)

    return driver
