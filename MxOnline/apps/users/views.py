# _*_ encoding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email


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
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:

                    login(request, user)
                    return render(request, "index.html", {})
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
