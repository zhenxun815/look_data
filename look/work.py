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


def get_hot():
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    wd.get('https://iplay.163.com/hot?livetype=2')
    links = []

    last_height = wd.execute_script("return document.body.scrollHeight")
    while True:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        new_height = wd.execute_script("return document.body.scrollHeight")
        link_elems = wd.find_elements_by_css_selector("a[href*=%s]" % 'live\\?')
        if new_height == last_height or len(link_elems) > 200:
            links.append([link_elem.get_property('href') for link_elem in link_elems])
            break
        last_height = new_height

    for link in links:
        print(f'get link: {link}')
        # wd.get(link)
        # print(f'{wd.page_source}')


if __name__ == '__main__':
    get_hot()
