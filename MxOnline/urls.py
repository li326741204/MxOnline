# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, ModifyPwdView
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="useractive"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetUserView.as_view(), name="userreset"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # 课程机构URL配置
    url(r'^org/', include('organization.urls', namespace="org")),
    # 配置上传图片的访问处理函数1，settings.TEMPLATES  2，HTML + {{ MEDIA_URL }}  3，urls.py + serve
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

]
