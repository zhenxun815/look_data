#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: finder.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/21/2020 15:55
import re

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait

from utils import common_utils
from utils import collections_utils
from selenium import webdriver

from selenium.webdriver import ActionChains
from airtest.core.api import *
from look import anchor_collect


class Finder:
    def __init__(self, driver: webdriver):
        self.wd = driver
        self.waiter = WebDriverWait(self.wd, 20, 1)

    def enter_room(self, room_url):
        self.wd.get(room_url)

    def get_rank(self, rank_type=2):
        all_names = []
        failed_url = None
        try:
            rank_btn_xpath = f'//div[@id="top-panel"]/div/div[2]/div[1]/span[{rank_type}]'
            self.waiter.until(lambda x: x.find_element_by_xpath(rank_btn_xpath)).click()

            top3_names = self.waiter.until(lambda x: x.find_elements_by_xpath(
                    '//div[@id="top-panel"]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div'))

            # print(f'top3 length {len(top3_names)}')
            all_names.extend(top3_names)
            # click load more btn
            self.waiter.until(
                    lambda x: x.find_element_by_xpath('//div[@id="top-panel"]/div/div[2]/div[2]/div[2]')).click()

            rank_container = self.wd.find_element_by_xpath('//div[@id="top-panel"]/div/div[2]/div[2]/div[1]')

            ActionChains(self.wd).move_to_element(rank_container).perform()
            other_names_length = 0
            other_names = []
            for i in range(6):
                # print(f'scroll time {i}')
                self.wd.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', rank_container)
                time.sleep(2)
                other_names = self.waiter.until(
                        lambda x: x.find_elements_by_xpath('//span[starts-with(@class,"name")]'))
                if other_names_length < len(other_names):
                    other_names_length = len(other_names)
                else:
                    break
                # print(f'scroll other name length is {other_names_length}')

            # print(f'top3 names length is {len(top3_names)}')
            # print(f'other names length is {len(other_names)}')
            all_names.extend(other_names)
        except TimeoutException:
            print(f'TimeoutException when get rank in: {self.wd.current_url}')
            failed_url = self.wd.current_url
        except WebDriverException:
            print(f'other WebDriverException when get rank in: {self.wd.current_url}')
            failed_url = self.wd.current_url

        # print(f'all names length is {len(other_names)}')
        return all_names, failed_url


def is_aim_in(aim, names2judge):
    for name in names2judge:
        name = name.text
        # print(f'name to judge {aim} is {name}')
        if name.find(aim) > -1:
            print(f'find {aim} in name {name}')
            return True
    return False


def get_anchor_id(room_url):
    pattern = re.compile(r'.*\?id\=(?P<room_id>[0-9]+)\.*')
    matcher = pattern.match(room_url)
    room_id = matcher.group('room_id')
    # print(room_id)
    return room_id


def check_all_room(name_finder, room_urls, aim_name):
    room_aims = []
    failed_urls = []
    for room_url in room_urls:
        name_finder.enter_room(room_url)
        names, failed_url = name_finder.get_rank()
        if failed_url:
            failed_urls.append(failed_url)
            continue
        # print(f'name length is {len(names)}')
        if is_aim_in(aim_name, names):
            room_id = get_anchor_id(room_url)
            print(f'find {aim_name} in room: {room_id}')
            room_aims.append(room_id)
    return room_aims, failed_urls


def check_test_room(name_finder, test_room_url, aim_name):
    name_finder.enter_room(test_room_url)
    ranks, _ = name_finder.get_rank()
    print(f'ranks length is {len(ranks)}')
    if is_aim_in(aim_name, ranks):
        room_id = get_anchor_id(test_room_url)
        print(f'find {aim_name} in room: {room_id}')


if __name__ == '__main__':
    aim = 'KLyn'
    test_aim = '炫迈'
    test_url = 'https://look.163.com/live?id=173539365'

    wd = common_utils.init_driver(headless=False)
    listen_room_urls = anchor_collect.collect_anchor_rooms(2, 200, wd)
    finder = Finder(wd)
    room_aims_to_check, try_again_urls = check_all_room(finder, listen_room_urls, test_aim)

    listen_room_urls = try_again_urls
    rooms = room_aims_to_check
    while len(listen_room_urls) > 0:
        room_aims_to_check, try_again_urls = check_all_room(finder, listen_room_urls, test_aim)
        listen_room_urls = try_again_urls
        rooms.extend(room_aims_to_check)

    collections_utils.print_list(rooms)
    # check_test_room(finder, test_url, test_aim)
    # wd.quit()
