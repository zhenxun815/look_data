#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: MoneyHunter.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/15/2020 12:04
import time

from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import NoSuchElementException

from lucky_money import driver_utils
from datetime import datetime
from appium import webdriver

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class MoneyHunter:

    def __init__(self, phone_number, password, is_emulator):
        print(f'hunter {phone_number} init...')
        self.phone_number = phone_number
        self.password = password
        self.is_emulator = is_emulator

    def auth(self):
        print('start auth...')
        driver_utils.waiting_element(waiter, 'com.netease.play:id/grant').click()
        driver_utils.waiting_element(waiter, 'android:id/button1').click()
        time.sleep(2)
        driver.find_element_by_id('android:id/button1').click()

    def login(self):
        print('into login step...')
        # agree the privacy policy and wait for the splash screen finish
        driver_utils.waiting_element(waiter, 'com.netease.play:id/btnConfirm').click()
        # time.sleep(10)

        print('start choose land mode...')
        # tap at [], to confirm the agreement
        driver_utils.waiting_element(waiter, 'com.netease.play:id/agreement')
        tap_point = (170, 1312) if self.is_emulator else (191, 1826)
        driver.tap([tap_point])

        # choose land mode
        driver.find_element_by_id('com.netease.play:id/phone').click()
        time.sleep(2)

        print(f'type in phone number and password...')
        driver.find_element_by_id('com.netease.play:id/phoneNumber') \
            .send_keys(self.phone_number)
        driver.find_element_by_id('com.netease.play:id/password') \
            .send_keys(self.password)
        driver.find_element_by_id('com.netease.play:id/login') \
            .click()

        print(f'into home activity..')
        print(f'confirm the youth mode notice..')
        driver_utils.waiting_element(waiter,
                                     'com.netease.play:id/youthModeBtn').click()

        # if is emulator, when update version notice appear, simulate pressing the back key
        if self.is_emulator:
            print('wait version update notice')
            driver_utils.waiting_element(waiter, 'com.netease.play:id/updateVersionContent')
            driver.keyevent(4)
            print('cancel version update...')

    def to_listen(self):
        print('into listen rooms')
        rooms = driver_utils.waiting_elements(waiter, 'com.netease.play:id/homecard')
        print(f'room num is {len(rooms)}')
        rooms[1].click()

    def to_live(self):
        print('into live rooms')
        driver.find_elements_by_class_name('androidx.appcompat.app.ActionBar$Tab')

    def watch_fly(self):

        # driver.implicitly_wait(10)

        try:
            webview_float = driver_utils.waiting_element(waiter, 'com.netease.play:id/webviewPendant')
            webview_float.find_element_by_id('com.netease.play:id/closeBtn').click()
            print(f'close web view float...')
        except NoSuchElementException:
            print(f'NoSuchElementException: webviewPendant')
        except Exception as e:
            print(f'Other Exception during search Notice: {e}')

        # waiting anchor recommend
        # print(f'waiting anchor recommend {datetime.today()}')
        # driver_utils.waiting_element(waiter, 'com.netease.play:id/useProfileCornerBg')
        # print(f'waiting anchor recommend {datetime.today()}')
        # tap_point = (700, 180) if self.is_emulator else (980, 253)
        # driver.tap([tap_point])

        print('start watching fly...')
        live_view = driver_utils.waiting_element(waiter, 'com.netease.play:id/liveViewerFragment')
        # driver.implicitly_wait(0.5)
        while True:
            try:
                print(f'search...{datetime.today()}')
                fly_container = driver.find_element_by_id('com.netease.play:id/liveNoticeContainer')
                fly_text = driver.find_element_by_id('com.netease.play:id/liveNotice').text
                print(f'fly appear...{fly_text}')
                if fly_text.find('红包'):
                    break
            except NoSuchElementException:
                print(f'NoSuchElementException: liveNoticeContainer')
            except InvalidElementStateException:
                print(f'InvalidElementStateException: liveNoticeContainer')
            except Exception as e:
                print(f'Other Exception during search Notice: {e}')
        # tap the fly
        tap_point = (700, 180) if self.is_emulator else (980, 253)
        driver.tap([tap_point])

        time.sleep(2)

        try:
            driver.find_element_by_id('com.netease.play:id/luckyMoneyEntryContainer').click()
            self.grap()
        except NoSuchElementException as e:
            print(f'NoSuchElementException: luckyMoneyEntryContainer')
        except Exception as e:
            print(e)

    def grap(self):
        print(f'waiting to grap {datetime.today()}')
        text = driver.find_element_by_id('com.netease.play:id/openButton').text
        print(f'time to click {text}')


memu_desired_caps = {
        'platformName':    'Android',
        'deviceName':      '127.0.0.1:21503',
        'appPackage':      'com.netease.play',
        'appActivity':     'com.netease.play.appstart.LoadingActivity',
        'platformVersion': '5.1.1'
}

miaomi_desired_caps = {
        'platformName':           'Android',
        'deviceName':             'bf005899',
        'appPackage':             'com.netease.play',
        'appActivity':            'com.netease.play.appstart.LoadingActivity',
        'platformVersion':        '9',
        'mjpegScreenshotUrl':     'http://192.168.1.211:8080/stream.mjpeg',
        'automationName':         'UiAutomator2',
        'ignoreUnimportantViews': True
}


def init_driver(is_emulator):
    desired_caps = memu_desired_caps if is_emulator else miaomi_desired_caps
    return webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


if __name__ == '__main__':

    is_emulator = False
    driver = init_driver(is_emulator)
    waiter = WebDriverWait(driver, timeout=30, poll_frequency=1)

    hunter1 = MoneyHunter('15255926026', '890815', is_emulator)
    if not is_emulator:
        hunter1.auth()
    hunter1.login()
    hunter1.to_listen()
    hunter1.watch_fly()
