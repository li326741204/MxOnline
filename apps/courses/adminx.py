# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-06 22:36'

import xadmin
from .models import Course, Lesson, Vedio, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'degree', 'course_org', 'teacher']
    search_fields = ['name', 'degree', 'course_org', 'teacher']
    list_filter = ['name', 'degree', 'course_org', 'teacher']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']  # 双下划线表示在过滤选项中显示该外键字段


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Vedio, VedioAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
