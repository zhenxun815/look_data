#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: money_hunter_real.py
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

miaomi_desired_caps = {
        'platformName':           'Android',
        'deviceName':             'bf005899',
        'appPackage':             'com.netease.play',
        'appActivity':            'com.netease.play.appstart.LoadingActivity',
        'platformVersion':        '9',
        # 'mjpegScreenshotUrl':     'http://192.168.1.211:8080/stream.mjpeg',
        'automationName':         'UiAutomator2',
        'ignoreUnimportantViews': True,
        'noReset':                True
}

Memu_desired_caps = {
        'platformName':           'Android',
        'deviceName':             '127.0.0.1:21503',
        'appPackage':             'com.netease.play',
        'appActivity':            'com.netease.play.appstart.LoadingActivity',
        'platformVersion':        '5.1.1',
        'automationName ':        'UiAutomator2',
        'ignoreUnimportantViews': True,
        'noReset':                True
}


def auth():
    print('start auth...')
    driver_utils.waiting_element(waiter, 'com.netease.play:id/grant').click()
    driver_utils.waiting_element(waiter, 'android:id/button1').click()
    time.sleep(2)
    driver.find_element_by_id('android:id/button1').click()


def login():
    print('into login step...')
    # agree the privacy policy and wait for the splash screen finish
    driver_utils.waiting_element(waiter, 'com.netease.play:id/btnConfirm').click()
    # time.sleep(10)

    print('start choose land mode...')
    # tap at [], to confirm the agreement
    driver_utils.waiting_element(waiter, 'com.netease.play:id/agreement')
    driver.tap([(191, 1826)])

    # choose land mode
    driver.find_element_by_id('com.netease.play:id/phone').click()
    time.sleep(2)

    print(f'type in phone number and password...')
    driver.find_element_by_id('com.netease.play:id/phoneNumber') \
        .send_keys(phone_number)
    driver.find_element_by_id('com.netease.play:id/password') \
        .send_keys(password)
    driver.find_element_by_id('com.netease.play:id/login') \
        .click()

    print(f'into home activity..')
    print(f'confirm the youth mode notice..')
    driver_utils.waiting_element(waiter,
                                 'com.netease.play:id/youthModeBtn').click()


def to_listen():
    print('into listen rooms')
    rooms = driver_utils.waiting_elements(waiter, 'com.netease.play:id/homecard')
    print(f'room num is {len(rooms)}')
    rooms[1].click()


def to_live():
    print('into live rooms')
    driver.find_elements_by_class_name('androidx.appcompat.app.ActionBar$Tab')


def close_web_float(root_container):
    print('try close web float...')
    try:
        time.sleep(3)
        selector = 'resourceId("com.netease.play:id/webviewPendant").childSelector(className("android.widget.ImageView"))'
        # webview_float = driver.find_element_by_android_uiautomator('resourceId("com.netease.play:id/webviewPendant")')
        print('float find...')
        # webview_float.find_element_by_id('com.netease.play:id/closeBtn').click()
        root_container.find_element_by_android_uiautomator(selector).click()
        print(f'close web view float...')
    except NoSuchElementException:
        print(f'NoSuchElementException: webviewPendant')
    except Exception as e:
        print(f'Other Exception during search Notice: {e}')


def watch_fly(root_container):
    # driver.implicitly_wait(10)

    print('start watching fly...')

    while True:
        try:
            print(f'search...{datetime.today()}')
            fly_text = root_container.find_element_by_id('com.netease.play:id/liveNotice').text
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
    driver.tap([(980, 253)])

    time.sleep(2)

    try:
        driver_utils.waiting_element(waiter, 'com.netease.play:id/luckyMoneyEntryContainer').click()
        grap()
    except NoSuchElementException as e:
        print(f'NoSuchElementException: luckyMoneyEntryContainer')
    except Exception as e:
        print(e)


def grap():
    print(f'waiting to grap {datetime.today()}')
    text = driver.find_element_by_id('com.netease.play:id/openButton').text
    print(f'time to click {text}')


def init_driver():
    desired_caps = miaomi_desired_caps
    return webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


def enter_room_by_search_id(room_id):
    print(f'start search room with id {room_id}')
    # click search button
    driver_utils.waiting_clickable(waiter, 'com.netease.play:id/iv_home_header_search').click()
    # type in room id
    driver_utils.waiting_element(waiter, 'com.netease.play:id/search_src_text').send_keys(room_id)
    # click confirm button
    driver.tap([(994, 1831)])
    # enter the room
    # driver_utils.waiting_element(waiter,'com.netease.play:id/liveStatus')
    driver.tap([(110, 350)])
    time.sleep(5)
    return driver.find_element_by_android_uiautomator('resourceId("com.netease.play:id/liveViewerFragment")')


if __name__ == '__main__':

    phone_number = '15255926026'
    password = '890815'
    driver = init_driver()
    waiter = WebDriverWait(driver, timeout=30, poll_frequency=1)

    # auth()
    # login()
    root_container = enter_room_by_search_id('269906754')
    close_web_float(root_container)
    # to_listen()
    watch_fly(root_container)
