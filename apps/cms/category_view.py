from django.views.generic import View
from .forms import CategoryForm, CategoryEditForm
from apps.poster.models import Category
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class CategoryView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                if request.user.is_superuser:
                    Category.objects.create(name=name)
                return redirect(reverse("cms:category_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改Category
        elif 'modify' in request.POST:
            form = CategoryEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                name = form.cleaned_data.get('name')
                if request.user.is_superuser:
                    Category.objects.filter(id=pk).update(name=name)
                return redirect(reverse("cms:category_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:category_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:category_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class CategoryEditView(View):
    def get(self,request):
        category_id = request.GET.get('category_id')
        category = Category.objects.get(pk=category_id)
        context = {
            'item_data': category,
        }
        return render(request, 'cms/category/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class CategoryDeleteView(View):
    def post(self,request):
        category_id = request.POST.get('category_id')
        if request.user.is_superuser:
            Category.objects.filter(id=category_id).delete()
        return restful.ok()