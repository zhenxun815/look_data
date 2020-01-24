#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: sniper.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/20/2020 15:39
# -*- encoding=utf8 -*-
from poco.exceptions import PocoTargetTimeout, PocoNoSuchNodeException
from datetime import datetime

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

auto_setup(__file__,
           devices=[
                   "Android://127.0.0.1:5037/127.0.0.1:21503?cap_method=JAVACAP^&^&ori_method=ADBORI",
           ])
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

FLAG_RESTART = 'restart'
FLAG_READY_GRAB = 'ready_grab'
FLAG_GRAB_SUCCESS = 'grab_success'
FLAG_UPDATE_CANCEL = 'update_cancel'

anchor = None


def close_web_float():
    web_close_btn = poco(name='com.netease.play:id/webviewPendant').child(name='com.netease.play:id/closeBtn')
    try:
        web_close_btn.wait_for_appearance(timeout=2)
        web_close_btn.click()
        print('web view float close...')
    except PocoTargetTimeout:
        print('web view float not find...')


def get_anchor_name(should_print=False):
    try:
        anchor_name = poco(name='com.netease.play:id/userName').get_text()
        if should_print:
            print(f'get anchor {anchor_name}')
        return anchor_name
    except PocoNoSuchNodeException:
        if should_print:
            print('anchor name not found, go to restart...')
        return None


def listen_notice():
    live_notice = poco(name='com.netease.play:id/liveNotice')
    get_name_fail = 0
    while True:
        print(f'watching fly notice...{datetime.today()}')
        if get_name_fail == 5:
            return FLAG_RESTART, anchor_name
        try:
            anchor_name = get_anchor_name()
            if anchor_name:
                get_name_fail = 0
                print(f'anchor name is {anchor_name}')
            else:
                get_name_fail += 1
                print(f'get anchor name fail...{get_name_fail}')
            live_notice.wait_for_appearance(10)
            notice_text = live_notice.get_text()
            print(f'notice is {notice_text}')
            if notice_text.find('红包') > -1:
                print('lucky money appear...')
                live_notice.parent().click(sleep_interval=2)
                return FLAG_READY_GRAB, anchor_name
            else:
                live_notice = poco(name='com.netease.play:id/liveNotice')
        except PocoTargetTimeout:
            print('live notice not appearance...')


def grab(lucky_money_container=None):
    print(f'ready to grab!')
    try:
        if not lucky_money_container:
            lucky_money_container = poco(name='com.netease.play:id/luckyMoneyEntryContainer')
            lucky_money_container.wait_for_appearance(10)
        lucky_money_container.click()
        try:
            open_btn = poco(name='com.netease.play:id/openButton')
            open_btn.wait_for_appearance(10)
            while True:
                open_btn = poco(name='com.netease.play:id/openButton')
                btn_text = open_btn.get_text()
                if '抢' == btn_text:
                    open_btn.click()
                    try:
                        result = poco(name='com.netease.play:id/resultGold')
                        result.wait_for_appearance(2)
                        result_text = result.get_text()
                        print(f'grab result is {result_text}')

                        close_btn = poco(name='com.netease.play:id/closeButton')
                        close_btn.click()
                        if poco(name='com.netease.play:id/luckyMoneyEntryContainer').exists():
                            grab()
                        return FLAG_GRAB_SUCCESS
                    except PocoTargetTimeout:
                        print('resultGold not appearance...')
                        return FLAG_RESTART
        except PocoTargetTimeout:
            print('openButton not appearance...')
        except PocoNoSuchNodeException:
            print('openButton not found...')

    except PocoTargetTimeout:
        print('luckyMoneyEntryContainer not appearance...')


def cancel_update():
    print('start cancel update version')
    try:
        update_notice = poco(name='com.netease.play:id/updateVersionBgImage')
        update_notice.wait_for_appearance(60)
        keyevent(keyname='BACK')
        print('update version canceled...')
        return FLAG_UPDATE_CANCEL
    except PocoTargetTimeout:
        print('update version not appearance...')
        return FLAG_RESTART


def to_listen():
    try:
        listen = poco(text='听听', type='android.widget.TextView')
        listen.wait_for_appearance(10)
        listen.click()
        print('to listen...')
    except PocoTargetTimeout:
        print('listen not appearance...')
        return FLAG_RESTART


def main_work_flow():
    # connect_device('Android://127.0.0.1:5037/127.0.0.1:21503?cap_method=JAVACAP')
    stop_app('com.netease.play')
    start_app('com.netease.play')

    update_flag = cancel_update()
    if FLAG_RESTART == update_flag:
        return

    to_listen()

    rooms = poco(name='com.netease.play:id/homecard')
    rooms.wait_for_appearance(10)
    # print(f'rooms count: {len(rooms)}')

    # avoid forbidden
    for i in range(1, len(rooms)):
        rooms[i].click()
        time.sleep(2)
        if get_anchor_name():
            break

    close_web_float()
    while True:
        flag, anchor = listen_notice()
        if FLAG_RESTART == flag:
            print('restart')
            break
        elif FLAG_READY_GRAB == flag:
            if anchor is not get_anchor_name():
                close_web_float()
            grab_flag = grab()
            if FLAG_RESTART == grab_flag:
                print('restart')
                break


if __name__ == '__main__':
    while True:
        main_work_flow()
