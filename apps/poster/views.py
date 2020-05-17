from django.shortcuts import render
from apps.poster.models import Post
# Create your views here.


def index(request):
    return render(request, 'post/index.html')


def detail(request, time_id):
    post = Post.objects.select_related('category', 'author').get(time_id=time_id)
    context = {
        'post_data': post,
    }

    return render(request, 'post/detail.html', context=context)