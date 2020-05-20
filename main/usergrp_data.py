# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  local_usergrp_data.py
@Description    :  
@CreateTime     :  2020/5/13 11:24
------------------------------------
@ModifyTime     :  
"""
import gc
import json
from api_zabbix import Zabbix
from local_api_cmdb import get_userGreop_data

url = "https://xxx.xsxs.com.cn/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
user = "xxxx"
password = "xxxxx"

zbx = Zabbix(url, user, password)

# cm_ugrp --> [{'product_code': u'PT00143', 'name': u'BPMS\u6d41\u7a0b\u5e73\u53f0'},...]
cm_ugrp = get_userGreop_data()
za_ugrp = json.loads(zbx.userGroup_Get(), strict=False)['result']
za_uglist = [{'usrgrpid': i.get('usrgrpid'), 'name': i.get('name')} for i in za_ugrp]

# 取zabbix中带产品编码的用户群组信息
za_ugdata = []
# za_ugdata --> [{'usrgrpid': u'15', 'code': u'CM00106', 'name': u'devops\u81ea\u52a8'},...]
for i in za_uglist[6:]:    # za_uglist[6:]: 去zabbix原有的用户群组
    dic = {'usrgrpid': i['usrgrpid']}
    code_name = i['name'].split('_')
    dic['code'] = code_name[0]
    dic['name'] = code_name[1]
    za_ugdata.append(dic)

za_ugtmp = [i['name'] for i in za_ugdata]
cm_ugtmp = [i['name'] for i in cm_ugrp]

# 批量创建用户群组，并校验用户数据是否重复
new_gname = []    # new_gname --> [{'product_code': u'PT00143','name': u'BPMS\u6d41\u7a0b\u5e73\u53f0'},...]
for i in cm_ugrp:
    if i['name'] not in za_ugtmp:
        new_gname.append({'product_code': i['product_code'], 'name': i['name']})
        zbx.userGroup_Create(ugrpname=(i['product_code'] + '_' + i['name']))

# zabbix批量同步删除cmdb已删除用户群组数据
del_gname = []
for i in za_ugdata:
    if i['name'] not in cm_ugtmp:
        del_gname.append({'product_code': i['code'], 'name': i['name']})
        zbx.userGroup_delete(ugrpid_list=[i['usrgrpid']])

gc.collect()