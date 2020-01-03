# _*_ encoding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite
from organization.models import CourseOrg


# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 激活选中图标
        course_page = "course"
        all_courses = Course.objects.all().order_by("-add_time")  # -号表示降序排列

        hot_courses = Course.objects.all().order_by("click_num")[:3]

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "courses":
                all_courses = all_courses.order_by("-click_num")

        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,  # 传入分页后的对象courses,在html中引用需要加入对象的object_list方法
            'sort': sort,
            'hot_courses': hot_courses,
            'course_page': course_page,
        })

    def post(self, request):
        pass


class CourseDetailView(View):
    # 课程详情页
    def get(self, request, course_id):
        # 课程相关子页面引用选中公开课图标
        course_page = 'course'

        course = Course.objects.get(id=int(course_id))
        # 课程点击数
        course.click_num += 1
        course.save()

        # 课程收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):  # 1表示课程收藏
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):  # 2表示机构收藏
                has_fav_org = True

        # 相关课程推荐，使用tag标签区别相关课程,默认显示2个相关课程
        course_tag = course.tag
        if course_tag:
            relate_courses = Course.objects.filter(tag=course_tag).order_by("-click_num")[:3]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'course_page': course_page,
        })

    def post(self, request):
        pass


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated():
            return HttpResponse('failed1')  # 用户未登录
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 若记录存在，表示用户取消收藏
            exist_records.delete()
            return HttpResponse("success1")  # 收藏
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('success2')  # 已收藏
            else:
                return HttpResponse('failed2')  # 收藏出错
