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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LookData:
    def __init__(self, base_url):
        self.wd = webdriver.Chrome()
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
            time.sleep(7)
            wd.find_element_by_tag_name('body').send_keys(Keys.HOME)
            wd.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(3)
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
        for link in links:
            print(f'request link {link}')
            wd.get(link)
            time.sleep(2)


if __name__ == '__main__':
    base_url = 'https://iplay.163.com/'
    worker = LookData(base_url)
    worker.landing()
    time.sleep(3)
    links = worker.get_hot(300)
    worker.wandering(links)
