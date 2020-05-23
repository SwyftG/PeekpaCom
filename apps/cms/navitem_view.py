from django.views.generic import View
from .forms import NavItemForm, NavItemEditForm
from apps.basefunction.models import NavbarItem
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class NavItemView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = NavItemForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url_path = form.cleaned_data.get('url_path')
                status = form.cleaned_data.get('status')
                show_page = form.cleaned_data.get('show_page')
                if request.user.is_superuser:
                    NavbarItem.objects.create(name=name, show_name=show_name, url_path=url_path, status=status, show_page=show_page)
                return redirect(reverse("cms:navitem_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改NavbarItem
        elif 'modify' in request.POST:
            form = NavItemEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url_path = form.cleaned_data.get('url_path')
                status = form.cleaned_data.get('status')
                show_page = form.cleaned_data.get('show_page')
                if request.user.is_superuser:
                    NavbarItem.objects.filter(id=pk).update(name=name, show_name=show_name, url_path=url_path, status=status, show_page=show_page)
                return redirect(reverse("cms:navitem_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:navitem_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:navitem_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class NavItemEditView(View):
    def get(self, request):
        navitem_id = request.GET.get('navitem_id')
        navitem = NavbarItem.objects.get(pk=navitem_id)
        context = {
            'item_data': navitem,
            'list_data_status': NavbarItem.STATUS_ITEMS,
            'list_data_show_page': NavbarItem.SHOW_PAGE_ITEMS,
        }
        return render(request, 'cms/navitem/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class NavItemDeleteView(View):
    def post(self, request):
        navitem_id = request.POST.get('navitem_id')
        if request.user.is_superuser:
            NavbarItem.objects.filter(id=navitem_id).update(status=NavbarItem.STATUS_DELETE)
        return restful.ok()
