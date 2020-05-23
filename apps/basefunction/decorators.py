# encoding: utf-8
from utils import restful
from django.shortcuts import redirect, reverse
from apps.basefunction.global_peekpa import check_url


def peekpa_url_check(func):
    def wrapper(request, *args, **kwargs):
        if check_url(request):
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='未授权！')
            else:
                return redirect(reverse('base:index'))
    return wrapper
