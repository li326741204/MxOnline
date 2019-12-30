# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse, JsonResponse
from courses.models import Course


# Create your views here.

class OrgView(View):
    """课程机构列表功能"""

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 筛选类别
        catgory = request.GET.get('ct', "")
        if catgory:
            all_orgs = all_orgs.filter(catgory=catgory)

        # 学习人数和课程数 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 传入筛选完之后的统计值
        org_nums = all_orgs.count()

        # 对课程机构列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {'all_orgs': orgs,  # 传入分页后的orgs对象
                                                 'all_citys': all_citys,
                                                 'org_nums': org_nums,
                                                 'city_id': city_id,
                                                 'catgory': catgory,
                                                 'hot_orgs': hot_orgs,
                                                 'sort': sort,
                                                 })


class AddUserAskView(View):
    def post(self, request):
        print(request.POST)
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('success')
        else:
            return HttpResponse('failed')


class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgCourseView(View):
    # 机构课程列表页
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgDescView(View):
    # 机构介绍页
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    # 机构讲师页
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,
            'current_page': current_page,
        })
