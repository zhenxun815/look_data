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
from lucky_money import KeyCode

emulator_desired_caps = {
        'platformName':           'Android',
        'deviceName':             '127.0.0.1:21503',
        'appPackage':             'com.netease.play',
        'appActivity':            'com.netease.play.appstart.LoadingActivity',
        'platformVersion':        '5.1.1',
        'automationName ':        'UiAutomator2',
        'ignoreUnimportantViews': True,
        'noReset':                True
}


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
        #selector = 'resourceId("com.netease.play:id/webviewPendant").childSelector(className("android.widget.ImageView"))'
        webview_float = root_container.find_element_by_android_uiautomator('resourceId("com.netease.play:id/webviewPendant")')
        print('float find...')
        webview_float.find_element_by_id('com.netease.play:id/closeBtn').click()
        #root_container.find_element_by_android_uiautomator(selector).click()
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
            print(f'watching fly...{datetime.today()}')
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
    driver.tap([(650, 170)])

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
    desired_caps = emulator_desired_caps
    return webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


def close_update():
    time.sleep(30)
    driver_utils.waiting_element(waiter, 'com.netease.play:id/updateVersionBtn')
    driver.keyevent(KeyCode.KEYCODE_BACK)


def enter_room_by_search_id(room_id):
    print(f'start search room with id {room_id}')
    # click search button
    driver_utils.waiting_clickable(waiter, 'com.netease.play:id/iv_home_header_search').click()
    # type in room id
    driver_utils.waiting_element(waiter, 'com.netease.play:id/search_src_text').send_keys(room_id)
    # click confirm button
    driver.keyevent(KeyCode.KEYCODE_ENTER)
    # enter the room
    # driver_utils.waiting_element(waiter,'com.netease.play:id/liveStatus')
    driver.tap([(75, 235)])
    return driver_utils.waiting_element(waiter,'com.netease.play:id/liveViewerFragment')


if __name__ == '__main__':

    phone_number = '15255926026'
    password = '890815'
    driver = init_driver()
    waiter = WebDriverWait(driver, timeout=30, poll_frequency=1)

    # auth()
    # login()
    close_update()
    root_container = enter_room_by_search_id('258357433')
    close_web_float(root_container)
    # to_listen()
    watch_fly(root_container)
