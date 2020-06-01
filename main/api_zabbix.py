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
@ModifyTime     :  2020/5/28 10:24
"""
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
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("获取Zabbix服务Token失败,请检查当前网络是否可用,或用户名及密码是否正确！！！")
        return resp.json().get("result")

    def user_Get(self):
        """
        获取用户信息
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
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("服务已断开,获取用户信息失败！！！")
        return resp.json()

    def host_Get(self):
        """
        获取主机信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend"
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("服务已断开,获取主机信息失败！！！")
        return resp.json()

    def hostname_Get(self, hostname):
        """
        获取主机信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter": {
                    "host": hostname if isinstance(hostname, list) else [hostname]
                },
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("服务已断开,获取指定主机信息失败！！！")
        return True if resp.json().get('result') else False

    def userGroup_Get(self):
        """
        获取用户群组信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.get",
            "params": {
                "output": "extend",
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("服务已断开,获取用户群组信息失败！！！")
        return resp.json()

    def hostGroup_Get(self, groupname=None):
        """
        获取主机群组信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
            },
            "auth": self.auth,
            "id": 1
        }
        if groupname:
            data["params"]["filter"] = {"name": groupname}
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("服务已断开,获取主机群组信息失败！！！")
        return resp.json().get("result")

    def user_Create(self, alias, name):
        """
        创建用户
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
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户创建失败")
        return resp.json()

    def host_Create(self, hostname, ip, group_id, template_id, name, proxy, dns="", port="20050", host_type=1):
        """
        创建主机
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "name": name,
                "host": hostname,
                "interfaces": [
                    {
                        "type": host_type,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": dns,
                        "port": port
                    }
                ],
                "groups": [{"groupid": group_id}],
                "templates": [{"templateid": template_id}],
                "proxy_hostid": proxy
            },
            "auth": self.auth,
            "id": 1
        }
        if not self.hostname_Get(hostname=hostname):
            return requests.post(url=self.url, json=data).json()
        else:
            print("主机实例已存在！！！")

    def userGroup_Create(self, ugrpname):
        """
        创建用户群组
        :param ugrpname: 用户群组名
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
        return resp.json()

    def hostGroup_Create(self, hgrpname):
        """
        创建主机群组
        :param hgrpname: 主机群组名
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": hgrpname
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户创建失败")
        return resp.json()

    def user_Delete(self, userid_list):
        """
        根据指定ID删除用户
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
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户删除失败")
        return resp.json()

    def host_Delete(self, hostid_list):
        """
        根据指定ID删除主机
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": hostid_list,
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("主机删除失败")
        return resp.json()

    def userGroup_Delete(self, ugrpid_list):
        """
        根据指定ID删除用户群组
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
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("用户群组删除失败")
        return resp.json()

    def hostGroup_Delete(self, hgrpid_list):
        """
        根据指定ID删除主机群组
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.delete",
            "params": hgrpid_list,
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        if resp.json().has_key("error") or resp.status_code != 200:
            raise BaseException("主机群组删除失败")
        return resp.json()

    def template_Get(self):
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
            },
            "auth": self.auth,
            "id": 1
        }
        resp = requests.post(url=self.url, json=data)
        return resp.json().get('result')
