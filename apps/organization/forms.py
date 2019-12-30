# _*_ coding: utf-8 _*_
__author__ = 'liliang'
__date__ = '2019-12-24 15:15'

import re
from django import forms
from operation.models import UserAsk


# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)

# ModelForm是Form的扩展，可以直接保存数据到库中，不用调用model的save方法
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # modelform的验证
    def clean_mobile(self):
        # 验证手机号码是否合法
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"非法号码",code="mobile_invalid")
