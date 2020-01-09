#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: Notifier.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/9/2020 9:57

import time
from datetime import datetime
from utils import common_utils


class Notifier:

    def __init__(self, room_id):
        self.room_id = room_id
        self.wd = common_utils.init_driver()
        self.wd.implicitly_wait(5)

    def watch(self):
        room_url = f'https://iplay.163.com/live?id={self.room_id}'
        live_flag = False

        self.wd.get(room_url)
        nick_name = self.wd.find_element_by_xpath('//div[contains(@class,"nickname")]').text
        while not live_flag:
            try:
                self.wd.refresh()
                span = self.wd.find_element_by_xpath('//div/span[contains(text(), "- 直播间已关闭 -")]')
                print(f'{datetime.today()} {nick_name} {span.text}')
                time.sleep(5)
            except Exception as ex:
                live_flag = True
                print(ex)
                print(f'{nick_name} live start')


if __name__ == '__main__':
    aling_id = '246385145'
    test_id = '148834749'
    print(f'program start to watch room {aling_id}')
    notifier = Notifier(aling_id)
    notifier.watch()
