#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: Anchor.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/19/2020 11:44


class Anchor:

    def __init__(self, room_id: str, name=None):
        self.room_id = room_id
        self.name = name

    def to_dict(self):
        _dict = {}
        _dict.update(self.__dict__)
        return _dict
