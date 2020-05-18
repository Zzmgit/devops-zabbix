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
import json
import os

import pandas as pd
from api_zabbix import Zabbix
from api_cmdb import get_user_data
from api_mail import send_mail

url = "https://xxx.xxx.com.cn/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
user = "xxxx"
password = "aa@xxxxx"

zbx = Zabbix(url, user, password)
cm_user = get_user_data()
za_user = json.loads(zbx.user_Get())['result']
# 超级管理员名单
superAdmin = [{"id": "1", "name": "Admin"},
              {"id": "2", "name": "guest"},
              {"id": "3", "name": "zhanghuiyun02"},
              {"id": "4", "name": "zhongzhimou01"},
              {"id": "5", "name": "liangqiguang"},
              {"id": "6", "name": "wuyang40"},
              {"id": "7", "name": "zengjian15"},
              {"id": "8", "name": "zhoumingjie"},
              {"id": "9", "name": "apiuser"},
              {"id": "10", "name": "zhangzheming03"},
              {"id": "11", "name": "liuyicheng04"},
              {"id": "12", "name": "linting26"}]
# ['id': '1', 'name': 'zabbix']
za_ulist = []
for i in za_user:
    user_info = {'id': i['userid'], 'name': i['alias']}
    za_ulist.append(user_info)
# ['zabbix']
tmp = []
for i in za_ulist:
    tmp.append(i['name'])
# 去除超级管理员角色['id': '2', 'name': 'songxiang']
for i in superAdmin:
    if i in za_ulist:
        za_ulist.remove(i)

# 批量创建用户，并校验用户数据是否重复
new_name = []
for i in cm_user:
    if i not in tmp:
        # print 'new：', i
        new_name.append(i)
        print zbx.user_Create(alias=i, name=i)
# zabbix批量同步删除cmdb已删除数据
del_name = []
for i in za_ulist:
    if i['name'] not in cm_user:
        # print 'del：', i['name']
        del_name.append(i['name'])
        print zbx.user_Delete(userid_list=[i['id']])

writer = pd.ExcelWriter("z_user.xlsx")
del_df = pd.DataFrame(del_name)
new_df = pd.DataFrame(new_name)
del_df.to_excel(writer, sheet_name="del", header=None, index=False, )
new_df.to_excel(writer, sheet_name="new", header=None, index=False, )
writer.save()

msg = """
    <h2>通知</h2>
    <p>监控小组，本次CMDB用户数据同步存在数据变动，详情请查阅附件</a></p>
    """
root_dir = os.path.dirname(os.path.abspath('.'))
attache = os.path.join(root_dir, r'main\z_user.xlsx')
send_mail(body=msg, attachment=attache, attache_title='user_changed_data.xlsx')
