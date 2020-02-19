# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite
from courses.models import Course


# Create your views here.

class OrgView(View):
    """课程机构列表功能"""

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 继承base页面选中图标
        org_page = 'organization'

        # 机构搜索关键词
        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))

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
                                                 'org_page': org_page,
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
        # 判断用户是否收藏该机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 机构下所有课程
        all_courses = course_org.course_set.all()
        # 机构下所有教师
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    # 机构课程列表页
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        # 判断用户是否收藏该机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    # 机构介绍页
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否收藏该机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    # 机构讲师页
    def get(self, request, org_id):
        current_page = "orgteacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        # 判断用户是否收藏该机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    # 用户收藏,取消收藏
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


class TeacherView(View):
    def get(self, request):
        current_page = 'teacher'
        # 所有教师列表
        all_teachers = Teacher.objects.all()

        # 教师搜索关键词，页面点击搜索js操作在deco-common.js.search_click方法中
        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keyword) | Q(work_company__icontains=search_keyword) |
                Q(work_position__icontains=search_keyword)
            )

        # 人气排序，参数需传至HTML
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "height":
                all_teachers = all_teachers.order_by("-fav_nums")
            # elif sort == "lower":
            #     all_teachers = all_teachers.order_by("-click_num")

        # 讲师排行榜前3
        tea_charts = Teacher.objects.all().order_by("-click_num")[:3]

        tea_nums = all_teachers.count()
        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 每页显示4个
        p = Paginator(all_teachers, 4, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'tea_nums': tea_nums,
            'tea_charts': tea_charts,
            'current_page': current_page,
        })

    def post(self, request):
        pass


class TeacherDetailView(View):
    def get(self, request, tea_id):
        teacher = Teacher.objects.get(id=int(tea_id))
        teacher.click_num += 1
        teacher.save()
        # 教师所授课程
        tea_course = Course.objects.filter(teacher=teacher.id)

        # 收藏功能
        if request.user.is_authenticated():
            has_teacher_faved = False
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True
            has_org_faved = False
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        # 教师排行榜
        sort_teacher = Teacher.objects.filter(org=teacher.org.id).order_by("-click_num")[:5]
        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'tea_course': tea_course,
            'sort_teacher': sort_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })

    def post(self, request):
        pass
