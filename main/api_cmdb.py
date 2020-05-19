# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  api_cmdb.py
@Description    :
@CreateTime     :  2020/5/13 11:16
------------------------------------
@ModifyTime     :  2020/5/19 19:45
"""
import requests


class CMDB(object):
    _user = "XXXX"
    _content_type = "application/json"
    _host = "xxxxxx.xxxxxx-xxx.com"
    _org = "XXXX"
    _ip = "XX.XX.XX.XXX"
    _obj = None
    json_data = None

    def __init__(self, obj, fields=None, query=None, page_size=500, debug=False):
        self.headers = {
            "host": self._host,
            "user": self._user,
            "org": self._org,
            "content-type": self._content_type
        }
        self._debug = debug
        self._obj = obj
        self.url = "http://" + self._ip + "/object/" + self._obj + "/instance/_search"
        self._get_param(fields, query, page_size)
        self._get_all_data()

    def _get_param(self, fields, query, page_size):
        """
        拼装请求信息
        :param fields:
        :param query:
        :param page_size:
        :return:
        """
        self.param = {}
        if isinstance(fields, list):
            self.param["fields"] = {}
            for i in fields:
                self.param["fields"][i] = True
        elif isinstance(fields, dict):
            self.param["fields"] = fields
            return
        self.param["query"] = query
        self.param["page_size"] = page_size
        self.param["page"] = 1

    def _get_all_data(self, method="post"):
        """
        获取所有数据信息方法
        :param method: 请求对应方法
        :return:
        """
        result = requests.request(method=method, headers=self.headers, url=self.url, json=self.param)
        if not result.status_code == 200:
            raise requests.ConnectionError(result.json()["error"])
        self.data = []
        result = result.json()
        self.data.extend(result["data"]["list"])
        self.total = result["data"]["total"]
        if self._debug:
            return
        num = self.param["page_size"]
        if self.total > num:
            for i in range(self.param["page"] + 1, int(self.total / num) + 2):
                self.param["page"] = i
                result = requests.request(method=method, headers=self.headers, url=self.url, json=self.param).json()
                self.data.extend(result["data"]["list"])


def get_user_data():
    """
    获取cmdb所有用户信息
    :return: [{'alias': 'xxx', 'name': 'xxx'}]
    """
    user_data = CMDB("USER", ["name", "nickname"], page_size=1000).data
    # # 原始for循环写法
    # user_list = []
    # for i in user_data:
    #     user_list.append({'name': i.get('nickname'), 'alias': i.get('name')})
    # return user_list
    # 列表推导式写法
    return [{'name': i.get('nickname'), 'alias': i.get('name')} for i in user_data]


def get_userGreop_data():
    """
    获取cmdb所有应用系统信息
    :return: [{'product_code': 'xxx', 'name': 'xxx'}]
    """
    ugrp_data = CMDB("BUSINESS", ["name", "product_code"], page_size=1000).data
    # # 原始for循环写法
    # ugrp_list = []
    # for i in ugrp_data:
    #     ugrp_list.append({"product_code": i.get('product_code'), "name": i.get('name')})
    # return ugrp_list
    # 列表推导式写法
    return [{"product_code": i.get('product_code'), "name": i.get('name')} for i in ugrp_data]
