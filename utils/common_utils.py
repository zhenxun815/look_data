#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: common_utils.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/9/2020 16:53

import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_driver(headless=True):
    """

    yum install google-chrome-stable
    yum install chromedriver

    ini the chrome webdriver
    :param driver_path:
    :param headless:
    :return:
    """
    sys_name = platform.system()
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    if headless:
        chrome_options.add_argument('--headless')

    print(f'init chrome webdriver on {sys_name}...')
    return webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
    init_driver('')
