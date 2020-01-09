#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: collections_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 9/24/2019 10:46


def print_list(alist: list, print_commont='', print_index=False):
    if print_index:
        for index, item in enumerate(alist):
            print(f'{print_commont} index: {index}, item: {item}')
    else:
        for item in alist:
            print(f'{print_commont} {item}')


def print_dict(adict: dict, work):
    for k, v in adict.items():
        print(f'k:{k}, v:{work(v)}')
