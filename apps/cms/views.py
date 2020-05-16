from django.shortcuts import render
from apps.poster.models import Category, Tag, Post
from apps.peekpauser.models import User
from .forms import PostForm

# Create your views here.


def cms_login(request):
    return render(request, 'cms/login.html')


def cms_dashboard(request):
    return render(request, 'cms/home.html')


def category_manage_view(request):
    context = {
        "list_data": Category.objects.all()
    }
    return render(request, 'cms/category/manage.html', context=context)


def category_publish_view(request):
    return render(request, 'cms/category/publish.html')


def tag_manage_view(request):
    context = {
        "list_data": Tag.objects.all()
    }
    return render(request, 'cms/tag/manage.html', context=context)


def tag_publish_view(request):
    return render(request, 'cms/tag/publish.html')


def post_manage_view(request):
    context = {
        "list_data": Post.objects.all()
    }
    return render(request, 'cms/post/manage.html', context=context)


def post_publish_view(request):
    context = {
        'list_data_category': Category.objects.all(),
        'list_data_tag': Tag.objects.all(),
        'list_data_user': User.objects.all(),
        'list_data_status': Post.STATUS_ITEMS
    }
    return render(request, 'cms/post/publish.html', context=context)