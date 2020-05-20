from django.shortcuts import render
from apps.poster.models import Post
from apps.base.common_view import get_read_most_post, get_exchange_link, get_navbar_item_homepage
# Create your views here.


def detail(request, time_id):
    post = Post.objects.select_related('category', 'author').get(time_id=time_id)
    context = {
        'post_data': post,
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    return render(request, 'post/detail.html', context=context)


def post_list_view(request):
    list_post = Post.objects.all()
    context = {
        'list_post': list_post
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    context.update(get_navbar_item_homepage())
    return render(request, 'post/list.html', context=context)
