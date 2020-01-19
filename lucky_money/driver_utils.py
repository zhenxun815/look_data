#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: driver_utils.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/15/2020 15:43
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def ec_element_clickable(element_id: str):
    """
    :param element_id:
    :return:
    """
    print(f'searching...  {datetime.today()}')
    locator = (By.ID, element_id)
    return EC.element_to_be_clickable(locator)


def ec_element_present(element_id: str):
    """
    :param element_id:
    :return: if present return the element else return a Exception
    """
    locator = (By.ID, element_id)
    return EC.presence_of_element_located(locator)


def ec_elements_present(element_id: str):
    """
    :param element_id:
    :return: if present return the element else return a Exception
    """
    locator = (By.ID, element_id)
    return EC.presence_of_all_elements_located(locator)


def waiting_clickable(waiter: WebDriverWait, element_id: str):
    return waiter.until(ec_element_clickable(element_id))


def waiting_element(waiter: WebDriverWait, element_id: str):
    """
    waiting element until it present, default max waiting time is 30 seconds,
    default poll interval is 1 seconds.
    :param waiter:
    :param element_id:
    :return:
    """
    return waiter.until(ec_element_present(element_id))


def waiting_elements(waiter: WebDriverWait, element_id: str):
    """
    waiting element until it present, default max waiting time is 30 seconds,
    default poll interval is 5 seconds.
    :param waiter:
    :param element_id:
    :return:
    """
    return waiter.until(ec_elements_present(element_id))
