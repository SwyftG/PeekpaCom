from django.views.generic import View
from .forms import TagForm, TagEditForm
from apps.poster.models import Tag
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class TagView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = TagForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                if request.user.is_superuser:
                    Tag.objects.create(name=name)
                return redirect(reverse("cms:tag_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改Tag
        elif 'modify' in request.POST:
            form = TagEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                name = form.cleaned_data.get('name')
                if request.user.is_superuser:
                    Tag.objects.filter(id=pk).update(name=name)
                return redirect(reverse("cms:tag_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:tag_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:tag_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class TagEditView(View):
    def get(self,request):
        tag_id = request.GET.get('tag_id')
        tag = Tag.objects.get(pk=tag_id)
        context = {
            'item_data': tag,
        }
        return render(request, 'cms/tag/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class TagDeleteView(View):
    def post(self,request):
        tag_id = request.POST.get('tag_id')
        if request.user.is_superuser:
            Tag.objects.filter(id=tag_id).delete()
        return restful.ok()