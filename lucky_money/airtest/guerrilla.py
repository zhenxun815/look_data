#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: guerrilla.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/24/2020 15:31
from poco.exceptions import PocoTargetTimeout, PocoNoSuchNodeException, PocoException
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
FLAG_CHANGE_SPACE = 'change_space'


def close_web_float():
    web_close_btn = poco(name='com.netease.play:id/webviewPendant').child(name='com.netease.play:id/closeBtn')
    try:
        web_close_btn.wait_for_appearance(timeout=2)
        web_close_btn.click()
        print('web view float close...')
    except PocoTargetTimeout:
        print('web view float not find...')


def to_space(space_flag):
    try:
        space_name = '听听' if space_flag % 2 == 0 else '看看'

        listen = poco(text=space_name, type='android.widget.TextView')
        listen.wait_for_appearance(5)
        listen.click()
        print(f'to space {space_name}...')
    except PocoTargetTimeout:
        print('not home page...')
        return FLAG_RESTART


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


def get_anchor_name(should_print=False):
    try:
        anchor_name_container = poco(name='com.netease.play:id/userName')
        anchor_name_container.wait_for_appearance(2)
        anchor_name = anchor_name_container.get_text()
        if should_print:
            print(f'get anchor {anchor_name}')
        return anchor_name
    except PocoNoSuchNodeException:
        if should_print:
            print('anchor name not found, go to restart...')
        return None


def swipe_to_next(space_flag=0):
    if space_flag % 2 == 0:
        print('swipe listen space...')
        swipe((0.8 * screen_width, 0.8 * screen_height),
              (0.8 * screen_width, 0.1 * screen_height),
              duration=0.5)
    else:
        print('swipe look space...')
        swipe((0.5 * screen_width, 0.4 * screen_height),
              (0, 0.3),
              duration=0.5)


def patrol(space_flag, patrol_round_time):
    # connect_device('Android://127.0.0.1:5037/127.0.0.1:21503?cap_method=JAVACAP')

    to_space_flag = to_space(space_flag)
    if to_space_flag:
        return to_space_flag

    rooms = poco(name='com.netease.play:id/homecard')
    rooms.wait_for_appearance(10)
    rooms[0].click()
    # print(f'rooms count: {len(rooms)}')

    # # avoid forbidden
    # for i in range(1, len(rooms)):
    #     rooms[i].click()
    #     time.sleep(2)
    #     if get_anchor_name():
    #         break

    patrol_round = 0
    while True:
        time.sleep(4)
        patrol_round += 1
        print(f'patrol in {space_flag % 2}, round {patrol_round}')
        if patrol_round > patrol_round_time:
            return FLAG_CHANGE_SPACE
        if get_anchor_name():
            close_web_float()
            lucky_money_container = poco(name='com.netease.play:id/luckyMoneyEntryContainer')
            try:
                lucky_money_container.wait_for_appearance(5)
                lucky_money_container.click()
                print(f'find container...')
                # if has followed, close record window
                result_gold = poco(name='com.netease.play:id/resultGold')
                time.sleep(2)
                if result_gold.exists():
                    print(f'has followed already, grab {result_gold.get_text()}')
                    poco(name='com.netease.play:id/closeButton').click()
                else:
                    try:
                        print(f'need to follow...')
                        follow_btn = poco(name='com.netease.play:id/button')
                        follow_btn.wait_for_appearance(5)
                        if follow_btn.exists():
                            if follow_btn.get_text().find('关注') > -1:
                                follow_btn.click()
                            while True:
                                follow_btn = poco(name='com.netease.play:id/button')
                                follow_text = follow_btn.get_text()
                                print(f'follow text is {follow_text}')
                                if follow_text.find('抢') > -1:
                                    follow_btn.click()
                                    break
                    except(PocoTargetTimeout, PocoException):
                        print('follow btn not appear...')

                    while True:
                        open_btn = poco(name='com.netease.play:id/openButton')
                        if open_btn.exists():
                            btn_text = open_btn.get_text()
                            # print(f'open text is {btn_text}')
                            if btn_text.find('抢') > -1:
                                open_btn.click(sleep_interval=2)
                                grab_result = poco(name='com.netease.play:id/resultGold').get_text()
                                print(f'grab over...{grab_result}')
                                break
                        else:
                            break
                poco(name='com.netease.play:id/closeButton').click()
            except (PocoTargetTimeout, PocoNoSuchNodeException):
                print('luckyMoneyEntryContainer not appearance,swipe to next room...')

            swipe_to_next(space_flag)
        else:
            return FLAG_RESTART


def restart_app():
    stop_app('com.netease.play')
    start_app('com.netease.play')

    update_flag = cancel_update()
    if FLAG_RESTART == update_flag:
        return


if __name__ == '__main__':
    screen_size = poco.get_screen_size()
    screen_width = screen_size[0]
    screen_height = screen_size[1]

    init_space = 1
    restart_app()
    while True:
        try:
            flag = patrol(init_space, patrol_round_time=20)
            if FLAG_CHANGE_SPACE == flag:
                print(f'back to home...')
                keyevent(keyname='BACK')
            elif FLAG_RESTART == flag:
                restart_app()
            init_space += 1
        except PocoTargetTimeout:
            print(f'PocoTargetTimeout....')
