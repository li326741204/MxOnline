# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-24 15:25'

from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherView, TeacherDetailView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    # 机构列表主页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    # 机构课程页
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    # 机构描述
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    # 机构教师
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构,教师收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),


    # 授课教师页
    url(r'^teacher/list/$', TeacherView.as_view(), name="teacher_list"),
    # 教师详情页
    url(r'^teacher_detail/(?P<tea_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

]
