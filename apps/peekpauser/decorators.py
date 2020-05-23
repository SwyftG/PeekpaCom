# encoding: utf-8
from utils import restful
from django.shortcuts import redirect, reverse


def peekpa_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')
            else:
                return redirect(reverse('cms:login'))
    return wrapper


def peekpa_login_superuser(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')
            else:
                return redirect(reverse('cms:login'))
    return wrapper
