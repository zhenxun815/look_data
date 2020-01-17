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
            # 'mjpegScreenshotUrl':     'http://192.168.1.213:8080/stream.mjpeg',
            'automationName':         'UiAutomator2',
            'ignoreUnimportantViews': True
    }

    def __init__(self, phone_number, password, is_emulator):
        print(f'hunter {phone_number} init...')
        self.phone_number = phone_number
        self.password = password
        self.is_emulator = is_emulator
        desired_caps = self.memu_desired_caps if is_emulator else self.miaomi_desired_caps
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def auth(self):
        print('start auth...')
        driver_utils.waiting_element(self.driver, 'com.netease.play:id/grant').click()
        driver_utils.waiting_element(self.driver, 'android:id/button1').click()
        time.sleep(2)
        self.driver.find_element_by_id('android:id/button1').click()

    def login(self):
        print('into login step...')
        # agree the privacy policy and wait for the splash screen finish
        driver_utils.waiting_element(self.driver, 'com.netease.play:id/btnConfirm').click()
        # time.sleep(10)

        print('start choose land mode...')
        # tap at [], to confirm the agreement
        driver_utils.waiting_element(self.driver, 'com.netease.play:id/agreement')
        tap_point = (170, 1312) if self.is_emulator else (191, 1826)
        self.driver.tap([tap_point])

        # choose land mode
        self.driver.find_element_by_id('com.netease.play:id/phone').click()
        time.sleep(2)

        print(f'type in phone number and password...')
        self.driver.find_element_by_id('com.netease.play:id/phoneNumber') \
            .send_keys(self.phone_number)
        self.driver.find_element_by_id('com.netease.play:id/password') \
            .send_keys(self.password)
        self.driver.find_element_by_id('com.netease.play:id/login') \
            .click()

        print(f'into home activity..')
        print(f'confirm the youth mode notice..')
        driver_utils.waiting_element(self.driver,
                                     'com.netease.play:id/youthModeBtn',
                                     interval=3).click()

        # if is emulator, when update version notice appear, simulate pressing the back key
        if self.is_emulator:
            print('wait version update notice')
            driver_utils.waiting_element(self.driver,
                                         'com.netease.play:id/updateVersionContent',
                                         max_wait=900,
                                         interval=10)
            self.driver.keyevent(4)
            print('cancel version update...')

    def to_listen(self):
        print('into listen rooms')
        rooms = driver_utils.waiting_elements(self.driver, 'com.netease.play:id/homecard')
        print(f'room num is {len(rooms)}')
        rooms[0].click()

    def to_live(self):
        print('into live rooms')
        self.driver.find_elements_by_class_name('androidx.appcompat.app.ActionBar$Tab')

    def watch_fly(self):

        # self.driver.implicitly_wait(10)
        print('start watching fly...')

        # self.driver.implicitly_wait(0.1)
        live_view = driver_utils.waiting_element(self.driver, 'com.netease.play:id/liveViewerFragment')
        self.driver.implicitly_wait(0.5)
        while True:
            try:
                print(f'search...{datetime.today()}')
                live_view.find_element_by_id('com.netease.play:id/liveNoticeContainer')
                print(f'fly appear...')
                break
            except NoSuchElementException as e:
                print(f'NoSuchElementException: liveNoticeContainer')
            except InvalidElementStateException as e:
                print(f'InvalidElementStateException: liveNoticeContainer')
            except Exception as e:
                print(f'Other Exception during search Notice: {e}')
        # tap the fly
        tap_point = (700, 180) if self.is_emulator else (980, 253)
        self.driver.tap([tap_point])

        time.sleep(2)
        tap_point = (700, 180) if self.is_emulator else (980, 253)
        self.driver.tap([tap_point])

        try:
            self.driver.find_element_by_id('com.netease.play:id/luckyMoneyEntryContainer').click()
            self.grap()
        except NoSuchElementException as e:
            print(f'NoSuchElementException: luckyMoneyEntryContainer')
            self.watch_fly()
        except Exception as e:
            print(e)

    def grap(self):
        print(f'waiting to grap {datetime.today()}')
        text = self.driver.find_element_by_id('com.netease.play:id/openButton').text
        print(f'time to click {text}')


if __name__ == '__main__':

    is_emulator = False
    hunter1 = MoneyHunter('15255926026', '890815', is_emulator=is_emulator)
    if not is_emulator:
        hunter1.auth()
    hunter1.login()
    hunter1.to_listen()
    hunter1.watch_fly()
