#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: MoneyHunter.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/15/2020 12:04
import time
from lucky_money import driver_utils

from appium import webdriver


class MoneyHunter:

    def __init__(self, phone_number, password):
        print(f'hunter {phone_number} init...')
        self.phone_number = phone_number
        self.password = password

        desired_caps = {
                'platformName':    'Android',
                'deviceName':      '127.0.0.1:21503',
                'appPackage':      'com.netease.play',
                'appActivity':     'com.netease.play.appstart.LoadingActivity',
                'platformVersion': '5.1.1'
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(30)

    def login(self):
        print('into login step...')
        # agree the privacy policy and wait for the splash screen finish
        self.driver.find_element_by_id('com.netease.play:id/btnConfirm').click()
        # time.sleep(10)

        print('start choose land mode...')
        # tap at [], to confirm the agreement
        driver_utils.waiting_element(self.driver, 'com.netease.play:id/agreement')
        self.driver.tap([(170, 1312)], 500)
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

        # when update version notice appear, simulate pressing the back key
        driver_utils.waiting_element(self.driver,
                                     'com.netease.play:id/updateVersionContent',
                                     interval=10)
        self.driver.keyevent(4)
        print('cancel version update...')

    def to_listen(self):
        print('into listen rooms')
        rooms = driver_utils.waiting_elements(self.driver, 'com.netease.play:id/homecard')
        print(f'room num is {len(rooms)}')
        rooms[0].click()

    def watch_fly(self):
        print('start watching fly')
        notice_container = driver_utils.waiting_element(self.driver, 'com.netease.play:id/liveNoticeContainer')
        notice = self.driver.find_element_by_id('com.netease.play:id/liveNotice')
        print(f'fly text is {notice.text}')
        notice_container.click()


if __name__ == '__main__':
    hunter1 = MoneyHunter('15255926026', '890815')
    hunter1.login()
    hunter1.to_listen()
