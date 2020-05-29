
from django import forms
from apps.base.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form, FormMixin):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20, min_length=6, error_messages={"max_length":"面最多不能超过20字符", "min_length":"密码最少不得少于6个字符"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6,
                               error_messages={"max_length": "面最多不能超过20字符", "min_length": "密码最少不得少于6个字符"})
    password2 = forms.CharField(max_length=20, min_length=6,
                               error_messages={"max_length": "面最多不能超过20字符", "min_length": "密码最少不得少于6个字符"})
    img_captcha = forms.CharField(min_length=4, max_length=4)
    sms_captcha = forms.CharField(min_length=4, max_length=4)

    def clean(self):
        clean_data = super(RegisterForm, self).clean()

        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        img_captcha = clean_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError('图形验证码失败')

        telephone = clean_data.get('telephone')
        sms_captcha = clean_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)
        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证失败')

        exists = User.objects.filter(telephone=telephone).exists ()
        if exists:
            raise forms.ValidationError('手机号码已存在')
