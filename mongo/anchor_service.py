#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: test.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/15/2019 10:30
import time

from pymongo import ASCENDING

from mongo.connect import get_collection


def find_by_room_id(room_id):
    query_filter = {
            'room_id': room_id
    }
    return get_collection('anchors').find_one(query_filter)


if __name__ == '__main__':
    clc_anchors = 'anchors'
    # remove_redundant('ip_doc', 'raw')
    start_time = time.time()
    # count = len(list(docs))
    # print('count is {}'.format(count))
    room = find_by_room_id('246385145')
    print(room)