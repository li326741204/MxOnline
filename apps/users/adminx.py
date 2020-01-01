# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-06 22:36'

import xadmin
from .models import EmailVerifyRecord, Banner, UserProfile
from xadmin import views


# 开通主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 全局功能设置
class GlobalSettings(object):
    site_title = "慕雪后台管理系统"  # 页标题
    site_footer = "慕雪在线网站"  # 页脚
    menu_style = "accordion"  # 菜单风格


class UserProfileAdmin(object):
    list_display = ['username', 'email', 'gender', 'mobile', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'gender', 'mobile', 'is_staff', 'is_active']
    list_filter = ['username', 'email', 'gender', 'mobile', 'is_staff', 'is_active']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    list_editable = ['code', 'email']  # 前台list_display页面字段右下角添加可直接编辑功能
    #model_icon = 'fa fa-envelope-open'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 取消注册功能
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册主题功能
xadmin.site.register(views.CommAdminView, GlobalSettings)
