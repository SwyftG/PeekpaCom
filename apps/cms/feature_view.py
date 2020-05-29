from django.views.generic import View
from .forms import FeatureForm, FeatureEditForm
from apps.basefunction.models import FeaturePost
from django.shortcuts import render, redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class FeatureView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = FeatureForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                url_path = form.cleaned_data.get('url_path')
                detail = form.cleaned_data.get('detail')
                status = form.cleaned_data.get('status')
                if request.user.is_superuser:
                    FeaturePost.objects.create(title=title, description=description, url_path=url_path, detail=detail, status=status)
                return redirect(reverse("cms:feature_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改 FeatureItem
        elif 'modify' in request.POST:
            form = FeatureEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                url_path = form.cleaned_data.get('url_path')
                detail = form.cleaned_data.get('detail')
                status = form.cleaned_data.get('status')
                if request.user.is_superuser:
                    FeaturePost.objects.filter(id=pk).update(title=title, description=description, url_path=url_path, detail=detail, status=status)
                return redirect(reverse("cms:feature_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:feature_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:feature_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class FeatureEditView(View):
    def get(self, request):
        feature_id = request.GET.get('feature_id')
        feature = FeaturePost.objects.get(pk=feature_id)
        context = {
            'item_data': feature,
            'list_data_status': FeaturePost.STATUS_ITEMS,
        }
        return render(request, 'cms/feature/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class FeatureDeleteView(View):
    def post(self, request):
        feature_id = request.POST.get('feature_id')
        if request.user.is_superuser:
            FeaturePost.objects.filter(id=feature_id).update(status=FeaturePost.STATUS_DELETE)
        return restful.ok()
