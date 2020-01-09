# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-06 22:36'

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'image', 'address', 'city']
    list_filter = ['name', 'image', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_position', 'points', 'add_time']
    search_fields = ['org', 'name', 'work_year', 'work_position', 'points']
    list_filter = ['org', 'name', 'work_year', 'work_position', 'points', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
