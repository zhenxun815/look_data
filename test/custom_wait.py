#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: custom_wait.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 11/13/2019 12:09

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait


class ElementHasCssClass(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://localhost:39527/html/test_upload.html")
    wait = WebDriverWait(driver, 10)
    elem = wait.until(ElementHasCssClass((By.ID, 'test'), "myCSSClass"))
    driver.execute_script('arguments[0].innerHTML = "Yiheng";', elem)
