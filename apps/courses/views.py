# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


# Create your views here.


class CourseListView(View):
    def get(self, request):
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
        })

    def post(self, request):
        pass


class CourseDetailView(View):
    # 课程详情页
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程点击数
        course.click_num += 1
        course.save()
        return render(request, 'course-detail.html', {
            'course': course,
        })

    def post(self, request):
        pass
