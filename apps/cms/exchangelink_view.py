from django.views.generic import View
from .forms import ExchangeLinkForm, ExchangeLinkEditForm
from apps.exchangelink.models import ExchangeLink
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class ExchangeLinkView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = ExchangeLinkForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url = form.cleaned_data.get('url')
                status = form.cleaned_data.get('status')
                if request.user.is_superuser:
                    ExchangeLink.objects.create(name=name, show_name=show_name, url=url, status=status)
                return redirect(reverse("cms:exchangelink_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改ExchangeLink
        elif 'modify' in request.POST:
            form = ExchangeLinkEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url = form.cleaned_data.get('url')
                status = form.cleaned_data.get('status')
                if request.user.is_superuser:
                    ExchangeLink.objects.filter(id=pk).update(name=name, show_name=show_name, url=url, status=status)
                return redirect(reverse("cms:exchangelink_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:exchangelink_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:exchangelink_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class ExchangeLinkEditView(View):
    def get(self, request):
        exchangelink_id = request.GET.get('exchangelink_id')
        exchangeLink = ExchangeLink.objects.get(pk=exchangelink_id)
        context = {
            'item_data': exchangeLink,
            'list_data_status': ExchangeLink.STATUS_ITEMS,
        }
        return render(request, 'cms/exchangelink/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class ExchangeLinkDeleteView(View):
    def post(self, request):
        exchangelink_id = request.POST.get('exchangelink_id')
        if request.user.is_superuser:
            ExchangeLink.objects.filter(id=exchangelink_id).update(status=ExchangeLink.STATUS_DELETE)
        return restful.ok()
