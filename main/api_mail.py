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
@ModifyTime     :  
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class SendMail(object):
    def __init__(self, host, user, pwd, sender, receiver, content=None, filepath=None, port=587, ):
        """
        邮件封装
        :param host: SMTP服务器地址
        :param user: 发送者账号
        :param pwd: 发送者密码
        :param sender: 发件人
        :param receiver: 收件人
        :param content: 邮件正文内容
        :param filepath: 附件
        :param port: 邮件服务器端口
        """
        self.host = host
        self.user = user
        self.pwd = pwd
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.filepath = filepath
        self.port = port

    def send_enclosure(self, filename, report_name):
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['From'] = Header("Zzm", 'utf-8')
        msg['To'] = Header("测试组", 'utf-8')
        subject = 'CMDB数据同步检测报告'
        msg['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        msg.attach(MIMEText(self.content, 'plain', 'utf-8'))

        # 构造附件
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # report_name可以任意写，写什么名字，邮件中显示什么名字
        # att["Content-Disposition"] = 'attachment; filename={}'.format(report_name)
        # 处理附件发送中文乱码问题
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', report_name))
        msg.attach(att)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.host, self.port)  # 25 为 SMTP 端口号
            smtpObj.login(self.user, self.pwd)
            smtpObj.sendmail(self.sender, self.receiver, msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: %s 无法发送邮件" % e)

    def __del__(self):
        pass


