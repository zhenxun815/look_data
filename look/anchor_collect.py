#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: anchor_collect.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 11/13/2019 15:58

# https://iplay.163.com/live?id=17922802&position=4
# https://iplay.163.com/live?id=191828770&position=8
import time

from selenium.webdriver import ActionChains

from utils import common_utils
from utils import collections_utils
from selenium.webdriver.common.keys import Keys


def collect_anchor_rooms(live_type, top_n, wd=None):
    host_url = 'https://iplay.163.com/'
    worker = AnchorCollector(host_url, wd)
    # worker.landing()
    # time.sleep(3)
    return worker.get_hot(live_type, top_n)


class AnchorCollector:
    def __init__(self, base_url, wd=None):

        self.wd = wd if wd else common_utils.init_driver()
        self.wd.implicitly_wait(10)
        self.base_url = base_url

    def get_hot(self, live_type=2, top_num=300):
        wd = self.wd
        wd.get(f'{self.base_url}hot?livetype={live_type}')

        elem = wd.find_element_by_id('CONTENT_ID')
        elem.click()
        curr_count = 0
        max_request = 0
        while True:
            # wd.find_element_by_tag_name('body').send_keys(Keys.HOME)
            # wd.find_element_by_tag_name('body').send_keys(Keys.END)
            content = wd.find_element_by_xpath('//div[@id="CONTENT_ID"]')
            ActionChains(self.wd).move_to_element(content).perform()
            wd.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', content)
            time.sleep(2)
            link_elems = wd.find_elements_by_css_selector("a[href*=%s]" % 'live\\?')
            elems_count = len(link_elems)
            if curr_count < elems_count:
                curr_count = elems_count
            else:
                if max_request == 5:
                    break
                wd.find_element_by_tag_name('body').send_keys(Keys.HOME)
                wd.find_element_by_tag_name('body').send_keys(Keys.END)
                max_request += 1
            # print(f'collect elem count {elems_count}')
            if elems_count > top_num:
                break
        print(f'final count{len(link_elems)}')
        return [link_elem.get_property('href') for link_elem in link_elems]


if __name__ == '__main__':
    driver = common_utils.init_driver(False)
    links = collect_anchor_rooms(2, 300, driver)
    collections_utils.print_list(links)
