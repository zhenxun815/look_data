#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: configs.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 12:05


class MongoConfigs:
    """configs of mongodb"""
    # uri configs
    db_host = 'localhost'
    db_port = 27017
    username = 'root'
    password = 'root'
    auth_source = 'admin'

    # db configs
    db_look_data = 'look_data'
    clc_anchor = 'anchor'
