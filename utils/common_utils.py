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


def init_driver(driver_path=None, headless=True):
    """
    ini the chrome webdriver
    :param driver_path:
    :param headless:
    :return:
    """
    sys_name = platform.system()
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')

    if 'Windows' == sys_name:
        print('init chrome webdriver on Windows...')
        return webdriver.Chrome(options=chrome_options)
    elif 'Linux' == sys_name and driver_path:
        print('init chrome webdriver on Linux...')
        return webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    else:
        print('init chrome webdriver fail...')
        return None


if __name__ == '__main__':
    init_driver('')
