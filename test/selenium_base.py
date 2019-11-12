#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: selenium_base.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 11/12/2019 10:14
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome()

    def test_search(self):
        driver = self.driver
        driver.get("https://www.baidu.com/")
        driver.implicitly_wait(10)
        print(f'title is: {driver.title}')
        assert "百度" in driver.title
        elem = driver.find_element_by_name("wd")
        elem.clear()
        elem.send_keys("Yiheng")
        print(f'elem is {elem.get_property("id")}')
        driver.find_element_by_id("su").click()

    def tearDown(self) -> None:
        driver = self.driver
        num = driver.window_handles
        print(f'num is {num}')
        # driver.switch_to.window(num[0])
        time.sleep(5)
        print(f'{self.driver.page_source}')
        driver.close()


if __name__ == '__main__':
    unittest.main()
