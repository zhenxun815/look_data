#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: json_encoder.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 15:47
from bson import ObjectId
import datetime
import json


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)

    def encode(self, o, ensure_ascii=False):
        self.ensure_ascii = ensure_ascii
        return super().encode(o)


encoder = JsonEncoder()


def doc2json(doc: dict, ):
    return encoder.encode(doc)


def docs2jsons(docs: list):
    return [encoder.encode(doc) for doc in docs]
