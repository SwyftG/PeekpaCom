# encoding: utf-8
from utils import restful
from django.shortcuts import redirect, reverse
from apps.basefunction.global_peekpa import check_code_session_by


def peekpa_code_required(func):
    def wrapper(request, *args, **kwargs):
        if check_code_session_by(request.session):
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='未授权！')
            else:
                return redirect(reverse('center:center_input_code'))
    return wrapper
