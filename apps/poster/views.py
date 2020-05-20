from django.shortcuts import render
from apps.poster.models import Post
from apps.exchangelink.models import ExchangeLink
# Create your views here.


def index(request):
    top_post = Post.objects.filter(is_main_page=True).order_by('-priority')
    list_post = Post.objects.filter(is_main_page=False)
    context = {
        'top_post': top_post,
        'list_post': list_post
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    return render(request, 'post/index.html', context=context)


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
    return render(request, 'post/list.html', context=context)


def get_read_most_post():
    read_post = Post.objects.all().order_by('-read_num')
    if len(read_post) > 5:
        read_post = read_post[:5]
    context = {
        'read_post': read_post
    }
    return context


def get_exchange_link():
    exchange_link = ExchangeLink.objects.filter(status=ExchangeLink.STATUS_NORMAL)
    context = {
        'exchange_link': exchange_link
    }
    return context