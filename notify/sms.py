#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: sms.py
# @Project: look_data
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/9/2020 18:23
# !/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send(phone_numbers, template_param):
    client = AcsClient('LTAI4Fhh9ZdVFw9mhYmUrfYM', 'Q51YfjaJWundhBJz2ADYqpZ5jn8v4y', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PhoneNumbers', phone_numbers)
    request.add_query_param('SignName', '小主驾到')
    request.add_query_param('TemplateCode', 'SMS_182535092')
    request.add_query_param('TemplateParam', '{\"code\":\"' + template_param + '\"}')

    response = client.do_action(request)
    # python2:  print(response)
    print(f'message response \n {str(response, encoding="utf-8")}')
