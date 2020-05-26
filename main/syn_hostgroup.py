# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  syn_hostgroup.py
@Description    :  
@CreateTime     :  2020/5/20 14:55
------------------------------------
@ModifyTime     :  2020/5/26 09:24
"""
import os
import gc
import json
import pandas as pd

from api_zabbix import Zabbix
from api_cmdb import get_host_data
from api_mail import send_mail

url = "https://xxx.xsxs.com.cn/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
user = "xxxx"
password = "xxxxx"

zbx = Zabbix(url, user, password)
cm_host = get_host_data()
cm_hgrp = list(set([i['product_code']+"_"+i['business'][0] for i in cm_host]))
za_hgrp = zbx.hostGroup_Get().get('result')
za_hglist = [{'hgrpid': i.get('groupid'), 'name': i.get('name')} for i in za_hgrp]

za_hgdata = []
for i in za_hglist:
    dic = {'hgrpid': i['hgrpid']}
    if '_' in str(json.dumps(i['name']).decode('utf-8')):
        code_name = i['name'].split('_')
        dic['code'] = code_name[0]
        dic['name'] = code_name[1]
        za_hgdata.append(dic)

cm_hgdata = []
for i in cm_hgrp:
    tmp = i.split('_')
    di = {'code': tmp[0], 'name': tmp[1]}
    cm_hgdata.append(di)

za_hgtmp = [i['name'] for i in za_hgdata]
cm_hgtmp = [i['name'] for i in cm_hgdata]

# 批量创建主机群组，并校验数据是否重复
new_gname = []
for i in cm_hgdata:
    if i['name'] not in za_hgtmp:
        new_gname.append({'code': i['code'], 'name': i['name']})
        print zbx.hostGroup_Create(hgrpname=(i['code'] + '_' + i['name']))

# zabbix批量同步删除cmdb已删除用户群组数据
del_gname = []
for i in za_hgdata:
    if i['name'] not in cm_hgtmp:
        del_gname.append({'code': i['code'], 'name': i['name']})

writer = pd.ExcelWriter("_hostgroup.xlsx")
del_df = pd.DataFrame(del_gname)
new_df = pd.DataFrame(new_gname)
del_df.to_excel(writer, sheet_name="del_hostgroup", header=None, index=False, )
new_df.to_excel(writer, sheet_name="new_hostgroup", header=None, index=False, )
writer.save()

msg = """
        <h2>主机群组数据同步通知：</h2>
        <p>监控小组注意，本次主机群组数据同步 "CMDB to Zabbix"，主机群组数据存在变更情况。具体变更数据，请查阅附件进行了解！</a></p>
      """
root_dir = os.path.dirname(os.path.abspath('.'))
attache = os.path.join(root_dir, r'main\_hostgroup.xlsx')
send_mail(body=msg, attachment=attache, attache_title='hostgroup_changed_data.xlsx')
gc.collect()
