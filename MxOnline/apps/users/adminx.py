# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-06 22:36'

import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views


# 开通主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 全局功能设置
class GlobalSettings(object):
    site_title = "慕雪后台管理系统"   # 页标题
    site_footer = "慕雪在线网站"   # 页脚
    menu_style = "accordion"    # 菜单风格


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册主题功能
xadmin.site.register(views.CommAdminView, GlobalSettings)
