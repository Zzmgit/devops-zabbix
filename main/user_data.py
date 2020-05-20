# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  user_data.py
@Description    :  
@CreateTime     :  2020/5/14 17:26
------------------------------------
@ModifyTime     :  
"""
import os
import gc
import json
import pandas as pd
from api_zabbix import Zabbix
from api_cmdb import get_user_data
from api_mail import send_mail

url = "https://xxx.xsxs.com.cn/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
user = "xxxx"
password = "xxxxx"

zbx = Zabbix(url, user, password)
# cm_user --> [{'alias': u'wenziwu', 'name': u'\u6e29\u6893\u92c8'},...]
cm_user = get_user_data()
za_user = json.loads(zbx.user_Get())['result']

za_ulist = [{'userid': i.get('userid'), 'alias': i.get('alias'), 'name': i.get('name')} for i in za_user]
# 将zabbix所有已有用户bip存为list --> [u'Admin', u'guest', u'apiuser', u'zhanghuiyun02',...]
za_tmp = [i['alias'] for i in za_ulist]
# 将cmdb所有已有用户bip存为list --> [u'wenziwu', u'caishanlun', u'chenjunxu02',...]
cm_tmp = [i['alias'] for i in cm_user]
print za_ulist[6:]
# 批量创建用户，并校验用户数据是否重复
new_name = []
for i in cm_user:
    if i['alias'] not in za_tmp:
        new_name.append({'BIP': i['alias'], 'name': i['name']})
        if i['name'] is not None:
            zbx.user_Create(alias=i['alias'], name=i['name'])
        else:
            zbx.user_Create(alias=i['alias'], name="None")

# zabbix批量同步删除cmdb已删除数据
del_name = []
for i in za_ulist[6:]:    # za_ulist[6:]去除Zabbix已有的超级管理员账号
    if i['alias'] not in cm_tmp:
        del_name.append({'BIP': i['alias'], 'name': i['name']})
        zbx.user_Delete(userid_list=[i['userid']])

writer = pd.ExcelWriter("user.xlsx")
del_df = pd.DataFrame(del_name)
new_df = pd.DataFrame(new_name)
del_df.to_excel(writer, sheet_name="del", header=None, index=False, )
new_df.to_excel(writer, sheet_name="new", header=None, index=False, )
writer.save()

msg = """
    <h2>通知：</h2>
    <p>监控小组，本次CMDB用户数据同步，存在数据变更。具体变更详情，请进行附件查阅！</a></p>
    """
root_dir = os.path.dirname(os.path.abspath('.'))
attache = os.path.join(root_dir, r'main\z_user.xlsx')
send_mail(body=msg, attachment=attache, attache_title='user_changed_data.xlsx')
gc.collect()
