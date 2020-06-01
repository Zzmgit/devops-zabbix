# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  syn_host.py
@Description    :  
@CreateTime     :  2020/5/26 9:51
------------------------------------
@ModifyTime     :  
"""
import random

from api_zabbix import Zabbix
from api_cmdb import get_host_data

url = "https://xxx.xsxs.com.cn/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
user = "xxxx"
password = "xxxxx"

zbx = Zabbix(url, user, password)
cm_host = get_host_data()
cm_hgrp = list(set([i['product_code'] + "_" + i['business'][0] for i in cm_host]))

# proxy server --> 10.208.10.227/228/229
proxy_list = ["10335", "10334", "10333"]

cm_tmp = []
for i in cm_hgrp:
    tmp = zbx.hostGroup_Get(groupname=i)
    if len(tmp):
        cm_tmp.append({"groupid": tmp[0].get("groupid"), "name": tmp[0].get("name")})

for i in cm_host:
    for k in cm_tmp:
        if (i['product_code'] + "_" + i['business'][0]) == k['name']:
            zbx.host_Create(hostname=i["hostname"], ip=i["ip"], group_id=k['groupid'],
                            template_id=("10001" if "Linux" in i["os"] else "10081"), name=i["vis_name"],
                            proxy=proxy_list[random.randint(0, 2)])
