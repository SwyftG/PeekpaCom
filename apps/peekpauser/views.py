from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from utils import restful
from .forms import LoginForm

# Create your views here.


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return redirect(reverse('cms:dashboard'))
            else:
                return restful.unauth(message="账号已经被冻结")
        else:
            # return restful_response.params_error(message="手机或者密码错误")
            return redirect(reverse('cms:login'))
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('cms:login'))