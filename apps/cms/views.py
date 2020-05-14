from django.shortcuts import render
from apps.poster.models import Category, Tag

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