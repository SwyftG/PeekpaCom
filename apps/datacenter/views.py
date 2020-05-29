from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST
# Create your views here.
from apps.base.common_view import get_navbar_item_homepage
from .decorators import peekpa_code_required
from apps.basefunction.global_peekpa import get_code_session
from apps.basefunction.decorators import peekpa_url_check
from .models import InputCode


@peekpa_url_check
def input_code_view(request):
    item = InputCode.objects.get_or_create(id=1)
    if item[1]:
        code = "代码"
    else:
        code = item[0].name
    context = {
        'code': code
    }
    context.update(get_navbar_item_homepage())
    return render(request, 'datacenter/input_code.html', context=context)


@require_POST
def validate_code(request):
    code = request.POST.get('form-code')
    session_name, session_uid = get_code_session(code)
    if session_uid and session_name:
        request.session[session_name] = session_uid
        request.session.set_expiry(0)
        return redirect(reverse("center:center_center_home_view"))
    else:
        return redirect(reverse("center:center_input_code"))


@peekpa_code_required
def center_home_view(request):
    context = {}
    context.update(get_navbar_item_homepage())
    return render(request, 'datacenter/home/center_home.html', context=context)