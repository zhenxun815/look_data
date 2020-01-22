#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: waiter.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/21/2020 10:56

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoTargetTimeout

auto_setup(__file__,
           devices=[
                   "Android://127.0.0.1:5037/127.0.0.1:21513?cap_method=JAVACAP^&^&ori_method=ADBORI",
           ])
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

if __name__ == '__main__':
    stop_app('com.happyteam.dubbingshow')
    start_app('com.happyteam.dubbingshow')
    focus_btn = poco(text='关注', type='android.widget.TextView').parent()
    try:
        focus_btn.wait_for_appearance(20)
        focus_btn.click()
    except PocoTargetTimeout:
        print('wait focus btn time out...')

    # check is anchor room living
    check_live_btn = poco(name="com.happyteam.dubbingshow:id/musicPlayView")
    try:
        check_live_btn.wait_for_appearance(3)
        check_live_btn.click(sleep_interval=2)
    except PocoTargetTimeout:
        print('wait check live btn time out...')

    not_live = poco(name='com.happyteam.dubbingshow:id/attention_live_empty')
    if not_live.exists():
        print('room not live...')
    else:
        online_names = poco(text='com.happyteam.dubbingshow:id/name', type='android.widget.TextView')
        for name in online_names:
            if name.get_text().find('爱好羽毛球') > -1:
                print(f'anchor room is living...')
                name.parent().parent().parent().click()
