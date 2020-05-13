# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  api_zabbix.py
@Description    :  
@CreateTime     :  2020/5/13 11:16
------------------------------------
@ModifyTime     :  
"""
import json
import requests


class Zabbix(object):

    def __init__(self, url, user, password):
        """
        初始化方法
        :param url: 接口调用地址
        :param user:
        :param password:
        """
        self.url = url
        self.auth = self._Login(user, password)

    def _Login(self, user, password):
        """
        私有化登录方法
        :param user:
        :param password:
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "id": 1,
            "auth": None,
            "params": {
                "user": user,
                "password": password
            }
        }
        # 请求结果
        resp = requests.post(url=self.url, json=data)
        auth = resp.json().get("result")
        return auth

    def userGroup_Create(self, ugrpname):
        """
        用户群组创建方法
        :param ugrpname:
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.create",
            "params": {
                "name": ugrpname,
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户群组创建失败")
        return json.dumps(resp.json()).decode('utf-8')

    def userGroup_Get(self):
        """
        用户群组信息获取
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.get",
            "params": {
                "output": "extend",
                # "usrgrpids": ugrpid,
                "status": 0
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return json.dumps(resp.json()).decode('unicode_escape')

    def userGroup_delete(self, ugrpid_list):
        """
        用户群组删除
        :param ugrpid_list:
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.delete",
            "params": ugrpid_list,
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return json.dumps(resp.json()).decode('utf-8')

    def userGroup_update(self, usrgrpid, usrgrpname):
        """
        用户群组改名
        :param usrgrpid: 用户群组ID
        :param usrgrpname: 用户群组名称
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.update",
            "params": {
                "usrgrpid": usrgrpid,
                "name": usrgrpname,
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return json.dumps(resp.json()).decode('utf-8')

    def user_Create(self, alias, name):
        """
        用户创建
        :param alias: 别名
        :param name: 用户名
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.create",
            "params": {
                "alias": alias,
                "name": name,
                "passwd": 'Bgy@user',
                "usrgrps": [{
                    "usrgrpid": "13"  # 默认CMDB用户群组
                }]
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        # 判断请求是否通过
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户创建失败")
        return json.dumps(resp.json()).decode('utf-8')

    def user_Get(self):
        """
        用户获取
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.get",
            "params": {
                "output": "extend"
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return json.dumps(resp.json()).decode('unicode_escape')

    def user_Delete(self, userid_list):
        """
        用户删除
        :param userid_list:
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.delete",
            "params": userid_list,
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return resp.json()
