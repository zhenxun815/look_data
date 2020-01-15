#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: driver_utils.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/15/2020 15:43
from appium.webdriver.webdriver import WebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def is_element_present(element_id: str):
    """
    :param element_id:
    :return: if present return the element else return a Exception
    """
    locator = (By.ID, element_id)
    return expected_conditions.presence_of_element_located(locator)


def is_elements_present(element_id: str):
    """
    :param element_id:
    :return: if present return the element else return a Exception
    """
    locator = (By.ID, element_id)
    return expected_conditions.presence_of_all_elements_located(locator)


def waiting_element(driver: WebDriver, element_id: str, max_wait=30):
    """
    waiting element until it present, default max waiting time is 30 second.
    :param driver:
    :param element_id:
    :param max_wait: unit is second
    :return:
    """
    WebDriverWait(driver, max_wait).until(is_element_present(element_id))
    return driver.find_element_by_id(element_id)


def waiting_elements(driver: WebDriver, element_id: str, max_wait=30):
    """
    waiting element until it present, default max waiting time is 30 second.
    :param driver:
    :param element_id:
    :param max_wait: unit is second
    :return:
    """
    WebDriverWait(driver, max_wait).until(is_elements_present(element_id))
    return driver.find_elements_by_id(element_id)