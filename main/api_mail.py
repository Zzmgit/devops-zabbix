# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzm
@Version        :  zhangzheming_zzm@foxmail.com
------------------------------------
@File           :  api_mail.py
@Description    :  
@CreateTime     :  2020/5/13 11:19
------------------------------------
@ModifyTime     :  2020/5/20 14:24
"""
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_mail(body, attachment=None, attache_title=None, type_='html'):
    style = """<style>
        table,table tr th, table tr td { border:1px solid black; }
        table { width: 200px; min-height: 25px; line-height: 25px;
        text-align: center; border-collapse: collapse; padding:2px;}
    </style>"""

    MAIL_CONFIG = {
        'host': 'smtp.xxxx.com.cn',
        'port': 'xx',
        'user': 'xxxx',
        'password': 'xxxx',
        'sender': 'xxxxx',
        'receiver': ['xxxxx', ]
    }

    # 创建一个带附件的实例
    msg = MIMEMultipart()
    msg['From'] = Header("Zzm", 'utf-8')
    msg['To'] = Header("Py收件机器人", 'utf-8')
    subject = '数据同步检测报告'
    msg['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    if type_ == 'html':
        msg.attach(MIMEText(style + body, type_, 'utf-8'))
    else:
        msg.attach(MIMEText(body, type_, 'utf-8'))

    # 构造附件
    if attachment is not None:
        att = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # report_name为自定义的附件标题,处理附件发送中文乱码问题
        # att["Content-Disposition"] = 'attachment; attachment={}'.format(attache_title)
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attache_title))
        msg.attach(att)

    try:
        smtpObj = smtplib.SMTP()
        # 连接SMTP服务器
        smtpObj.connect(MAIL_CONFIG['host'], MAIL_CONFIG['port'])  # 25 为 SMTP 端口号
        # 邮件用户登录
        smtpObj.login(MAIL_CONFIG['user'], MAIL_CONFIG['password'])
        # 发送带附件的邮件
        smtpObj.sendmail(MAIL_CONFIG['sender'], MAIL_CONFIG['receiver'], msg.as_string())
        print("邮件发送成功...")
    except smtplib.SMTPException as e:
        print("Error: %s 无法发送邮件!!!" % e)


# 测试
msg = """
        <h2>测试表</h2><br/>
        <table border="1">
            <tr>
                <td>编号</td>
                <td>项目</td>
            </tr>
            <tr>
                <td>{0}</td>
                <td>{1}</td>
            </tr>
        </table>
    """.format(1001, 'test data')
root_dir = os.path.dirname(os.path.abspath('.'))
path = os.path.join(root_dir, r'main')
attache = os.path.join(root_dir, r'main\z.xlsx')
# send_mail(body=msg, attachment=attache, attache_title='changed_data.xlsx')
