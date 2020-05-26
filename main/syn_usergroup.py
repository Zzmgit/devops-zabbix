# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  local_usergroup_data.py
@Description    :  
@CreateTime     :  2020/5/13 11:24
------------------------------------
@ModifyTime     :  2020/5/20 14:24
"""
import os
import gc
import json
import pandas as pd

from api_zabbix import Zabbix
from api_cmdb import get_userGreop_data
from api_mail import send_mail

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
        new_gname.append({'code': i['product_code'], 'name': i['name']})
        zbx.userGroup_Create(ugrpname=(i['product_code'] + '_' + i['name']))

# zabbix批量同步删除cmdb已删除用户群组数据
del_gname = []
for i in za_ugdata:
    if i['name'] not in cm_ugtmp:
        del_gname.append({'code': i['code'], 'name': i['name']})
        zbx.userGroup_delete(ugrpid_list=[i['usrgrpid']])

writer = pd.ExcelWriter("usergroup.xlsx")
del_df = pd.DataFrame(del_gname)
new_df = pd.DataFrame(new_gname)
del_df.to_excel(writer, sheet_name="del_usergroup", header=None, index=False, )
new_df.to_excel(writer, sheet_name="new_usergroup", header=None, index=False, )
writer.save()

msg = """
    <h2>用户群组数据同步通知：</h2>
    <p>监控小组注意，本次用户群组数据同步 "CMDB to Zabbix"，用户群组数据存在变更情况。具体变更数据，请查阅附件进行了解！</a></p>
    """
root_dir = os.path.dirname(os.path.abspath('.'))
attache = os.path.join(root_dir, r'main\usergroup.xlsx')
send_mail(body=msg, attachment=attache, attache_title='usergroup_changed_data.xlsx')
gc.collect()
