# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-16 9:59'
from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from MxOnline.settings import DEFAULT_FROM_EMAIL


def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "liliang学习网注册激活链接"
        email_body = "点击链接激活账号: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "liliang学习网密码重置链接"
        email_body = "点击链接重置账号: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass
