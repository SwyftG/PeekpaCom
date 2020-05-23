from django.views.generic import View
from .forms import UserForm
from apps.peekpauser.models import User
from django.shortcuts import redirect, reverse
from utils import restful
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required, peekpa_login_superuser


@method_decorator(peekpa_login_required, name='post')
@method_decorator(peekpa_login_superuser, name='post')
class UserView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                User.objects.create_user(email=email, username=username, password=password)
                return redirect(reverse("cms:user_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 新建状态的取消
        else:
            return redirect(reverse("cms:navitem_publish_view"))


@method_decorator(peekpa_login_required, name='post')
@method_decorator(peekpa_login_superuser, name='post')
class UserDeleteView(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        User.objects.filter(uid=user_id).delete()
        return restful.ok()
