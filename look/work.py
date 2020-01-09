#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: work.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 11/13/2019 15:58

# https://iplay.163.com/live?id=17922802&position=4
# https://iplay.163.com/live?id=191828770&position=8
import time

from utils import common_utils
from selenium.webdriver.common.keys import Keys


class LookData:
    def __init__(self, base_url):
        self.wd = self.wd = common_utils.init_driver(headless=False)
        self.wd.implicitly_wait(10)
        self.base_url = base_url

    def landing(self):
        wd = self.wd
        wd.get(f'{self.base_url}hot?livetype=2')
        # call landing pop window
        wd.find_element_by_xpath('//div[@id="j-app"]/div[1]/div[3]').click()
        time.sleep(1)
        wd.find_element_by_xpath('//input[@placeholder="请输入手机号"]').send_keys('15255926026')
        wd.find_element_by_xpath('//input[@placeholder="请输入登录密码"]').send_keys('890815')
        wd.find_element_by_xpath('//div/p/label/span').click()
        time.sleep(1)
        # click landing
        wd.find_element_by_xpath('//div[@id="j-portal"]/div/div/div[2]/div/div/div/div[4]').click()

    def get_hot(self, top_num):
        wd = self.wd
        wd.get(f'{self.base_url}hot?livetype=2')

        elem = wd.find_element_by_id('CONTENT_ID')
        elem.click()
        curr_count = 0
        max_request = 0
        while True:
            wd.find_element_by_tag_name('body').send_keys(Keys.HOME)
            wd.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(10)
            link_elems = wd.find_elements_by_css_selector("a[href*=%s]" % 'live\\?')
            elems_count = len(link_elems)
            if curr_count < elems_count:
                curr_count = elems_count
            else:
                if max_request == 3:
                    break
                max_request += 1
            print(f'collect elem count {elems_count}')
            if elems_count > top_num:
                break
        print(f'final count{len(link_elems)}')
        return [link_elem.get_property('href') for link_elem in link_elems]

    def wandering(self, links: list):
        wd = self.wd
        links.insert(0, 'https://iplay.163.com/live?id=246385145')
        links.insert(0, 'https://iplay.163.com/live?id=257471368')
        links.insert(0, 'https://iplay.163.com/live?id=148834749')
        for link in links:
            print(f'request link {link}')
            wd.get(link)
            try:
                wd.find_element_by_xpath('//input[@placeholder="跟主播聊聊吧~"]').send_keys('喵~晚上好~')
                time.sleep(2)
                wd.find_element_by_xpath('//div[text()="发 送"]').click()
                time.sleep(5)
            except Exception as re:
                print(re)


if __name__ == '__main__':
    host_url = 'https://iplay.163.com/'
    worker = LookData(host_url)
    worker.landing()
    time.sleep(3)
    while True:
        links = worker.get_hot(300)
        worker.wandering(links)
