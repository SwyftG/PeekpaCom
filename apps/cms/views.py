from django.shortcuts import render
from apps.poster.models import Category, Tag, Post
from apps.exchangelink.models import ExchangeLink
from apps.peekpauser.models import User
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.http import require_POST

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
    page = int(request.GET.get('p', 1))
    posts = Post.objects.all()
    paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    page_obj = paginator.page(page)
    context = {
        "list_data": page_obj.object_list,
        'list_data_status': Post.STATUS_ITEMS,
        'url_tag_info': ['post', 'post.manage']
    }
    context_data = get_pagination_data(paginator, page_obj)
    context.update(context_data)
    return render(request, 'cms/post/manage.html', context=context)


def post_publish_view(request):
    context = {
        'list_data_category': Category.objects.all(),
        'list_data_tag': Tag.objects.all(),
        'list_data_user': User.objects.all(),
        'list_data_status': Post.STATUS_ITEMS,
        'url_tag_info': ['post', 'post.publish']
    }
    return render(request, 'cms/post/publish.html', context=context)


def get_pagination_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages

    left_has_more = False
    right_has_more = False

    if current_page <= around_count + settings.ONE_PAGE_NEWS_COUNT:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)

    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)

    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        'current_page': current_page,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'num_pages': num_pages
    }


def exchangelink_manage_view(request):
    context = {
        "list_data": ExchangeLink.objects.all(),
        'list_data_status': ExchangeLink.STATUS_ITEMS
    }
    return render(request, 'cms/exchangelink/manage.html', context=context)


def exchangelink_publish_view(request):
    context = {
        'list_data_status': ExchangeLink.STATUS_ITEMS
    }
    return render(request, 'cms/exchangelink/publish.html', context=context)