# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite
from organization.models import CourseOrg,Teacher
from courses.models import Course


# 使用邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                curr_reg_email = record.email
                curr_reg_user = UserProfile.objects.get(email=curr_reg_email)
                curr_reg_user.is_active = True
                curr_reg_user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, 'login.html')


class ResetUserView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {'email': email})
        else:
            return HttpResponse("链接无效")
        return render(request, 'login.html')


class ModifyPwdView(View):
    # 用户修改密码(未登录)
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pass1 = request.POST.get('password1', '')
            pass2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pass1 != pass2:
                return render(request, 'password_reset.html', {'msg': '密码输入不一致', 'email': email})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pass1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_pwd_form': modify_pwd_form, 'email': email})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '邮箱已存在', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            userprofile = UserProfile()
            userprofile.username = user_name
            userprofile.email = user_name
            userprofile.is_active = False
            userprofile.password = make_password(pass_word)
            send_register_email(user_name, 'register')
            userprofile.save()
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        index_page = 'index'
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    index_page = 'index'
                    login(request, user)
                    print(request.user)
                    return render(request, "index.html", {'index_page': index_page})
                else:
                    return render(request, 'login.html', {"msg": "用户未激活"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, "send_success.html")
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class UserInfoView(LoginRequiredMixin, View):
    # 用户个人信息
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    # 用户修改头像
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")


class UpdatePwdView(View):
    # 个人中心用户修改密码
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pass1 = request.POST.get('password1', '')
            pass2 = request.POST.get('password2', '')
            if pass1 != pass2:
                # json效果实现
                return HttpResponse('{"status":"failed", "msg":"密码一定不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pass1)
            user.save()
            # 效果实现
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # json效果实现
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    # 发送邮箱验证码
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"该邮箱已被注册"}', content_type='application/json')
        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class CheckEmailCodeView(LoginRequiredMixin, View):
    # 校验邮箱验证码
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码有误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    # 我的课程
    def get(self, request):
        user_course = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_course': user_course,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    # 我的收藏的课程机构
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    # 我的喜爱的授课讲师
    def get(self, request):
        tea_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_tea in fav_teachers:
            tea_id = fav_tea.fav_id
            teacher = Teacher.objects.get(id=tea_id)
            tea_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'tea_list': tea_list,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    # 我收藏的课程
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })