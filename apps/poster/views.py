from django.shortcuts import render
from apps.poster.models import Post
# Create your views here.


def index(request):
    top_post = Post.objects.filter(is_main_page=True).order_by('-priority')
    list_post = Post.objects.filter(is_main_page=False)
    context = {
        'top_post': top_post,
        'list_post': list_post
    }
    return render(request, 'post/index.html', context=context)


def detail(request, time_id):
    post = Post.objects.select_related('category', 'author').get(time_id=time_id)
    context = {
        'post_data': post,
    }
    return render(request, 'post/detail.html', context=context)