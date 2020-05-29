from django.shortcuts import render
from apps.poster.models import Post
from apps.base.common_view import get_exchange_link, get_read_most_post, get_navbar_item_homepage, get_feature_post_post
from apps.base.tracking_view import peekpa_tracking
# Create your views here.


@peekpa_tracking
def index(request):
    top_post = Post.objects.filter(is_main_page=True).order_by('-priority')
    list_post = Post.objects.filter(is_main_page=False)
    context = {
        'top_post': top_post,
        'list_post': list_post
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    context.update(get_navbar_item_homepage())
    context.update(get_feature_post_post())
    return render(request, 'post/index.html', context=context)