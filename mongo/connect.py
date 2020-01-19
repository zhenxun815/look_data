#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: connect.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 10:49

from pymongo import MongoClient
from mongo.configs import MongoConfigs
from mongo.model.Anchor import Anchor

import json


class Connect:
    @staticmethod
    def get_connection():
        username = MongoConfigs.username
        password = MongoConfigs.password
        host = MongoConfigs.db_host
        port = MongoConfigs.db_port
        auth_source = MongoConfigs.auth_source
        uri = 'mongodb://%s:%s@%s:%d/?authSource=%s' % (username, password, host, port, auth_source)
        return MongoClient(uri)


def get_db(db_name):
    """
    connect to mongo and get the param specified db
    :param db_name: the db's name
    :return:
    """
    return Connect.get_connection().get_database(db_name)  # same with: client[db_name]


def get_collection(clc_name, db_name='look_data'):
    """
    connect to mongo and get the param specified db's collection obj
    :param db_name:
    :param clc_name:
    :return:
    """
    db = get_db(db_name)
    return db.get_collection(clc_name)
