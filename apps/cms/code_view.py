from django.views.generic import View
from .forms import CodeForm, CodeEditForm
from apps.datacenter.models import Code
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required, peekpa_login_superuser


@method_decorator(peekpa_login_required, name='post')
@method_decorator(peekpa_login_superuser, name='post')
class CodeView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = CodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data.get('code')
                session_name = form.cleaned_data.get('session_name')
                status = form.cleaned_data.get('status')
                Code.objects.create(code=code, session_name=session_name, status=status)
                return redirect(reverse("cms:code_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改 Code
        elif 'modify' in request.POST:
            form = CodeEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                code = form.cleaned_data.get('code')
                session_name = form.cleaned_data.get('session_name')
                status = form.cleaned_data.get('status')
                Code.objects.filter(uid=pk).update(code=code, session_name=session_name, status=status)
                return redirect(reverse("cms:code_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:code_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:code_publish_view"))


@method_decorator(peekpa_login_required, name='get')
@method_decorator(peekpa_login_superuser, name='get')
class CodeEditView(View):
    def get(self, request):
        code_id = request.GET.get('code_id')
        code = Code.objects.get(uid=code_id)
        context = {
            'item_data': code,
            'list_data_status': Code.STATUS_ITEMS,
        }
        return render(request, 'cms/code/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
@method_decorator(peekpa_login_superuser, name='post')
class CodeDeleteView(View):
    def post(self, request):
        code_id = request.POST.get('code_id')
        Code.objects.filter(uid=code_id).update(status=Code.STATUS_DELETE)
        return restful.ok()
