# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-24 15:25'
from .views import CourseListView, CourseDetailView, AddFavView, CourseVideoView, VideoCommentView, AddCommentView
from django.conf.urls import url

urlpatterns = [
    # 课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 视频详情
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),

    # 视频评论
    url(r'^comment/(?P<course_id>\d+)/$', VideoCommentView.as_view(), name="course_comment"),

    # 发送评论
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),

]
