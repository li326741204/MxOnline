# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-13 14:11'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
