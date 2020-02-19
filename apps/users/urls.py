# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-24 15:25'

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, CheckEmailCodeView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView

urlpatterns = [
    # 用户信息首页
    url('^info/$', UserInfoView.as_view(), name="user_info"),

    # 用户头像上传
    url('^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # 用户修改密码
    url('^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    # 修改邮箱发送验证码
    url('^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱校验验证码
    url('^checkemail_code/$', CheckEmailCodeView.as_view(), name="checkemail_code"),

    # 我的课程
    url('^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    # 我收藏的课程机构
    url('^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的授课讲师
    url('^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我收藏的课程
    url('^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

]
