# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-24 15:25'
from .views import CourseListView, CourseDetailView
from django.conf.urls import url

urlpatterns = [
    # 课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
]
