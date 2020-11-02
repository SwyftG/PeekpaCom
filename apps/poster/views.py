import markdown
from django.db.models import F
from django.shortcuts import render
from apps.poster.models import Post
from django.core.cache import cache
from apps.base.common_view import get_read_most_post, get_exchange_link, get_navbar_item_homepage
from apps.base.tracking_view import peekpa_tracking
# Create your views here.


@peekpa_tracking
def detail(request, time_id):
    post = Post.objects.select_related('category', 'author').get(time_id=time_id)
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    # post.content_html = md.convert(post.content)
    md.convert(post.content)
    context = {
        'post_data': post,
        'toc': process_toc(md.toc)
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    context.update(get_navbar_item_homepage())
    handle_visited(request, time_id)
    return render(request, 'post/detail.html', context=context)

def process_toc(toc):
    toc = toc.replace('<div class="toc">', '').replace('</div>','').replace('<ul>','<ul class="list-group">').replace('<li>','<li class="list-group-item">')
    return toc

@peekpa_tracking
def post_list_view(request):
    list_post = Post.objects.all()
    context = {
        'list_post': list_post
    }
    context.update(get_read_most_post())
    context.update(get_exchange_link())
    context.update(get_navbar_item_homepage())
    return render(request, 'post/list.html', context=context)


def handle_visited(request, time_id):
    increase_post_view = True
    uid = request.uid
    pv_key = 'pv:%s:%s' % (uid, request.path)
    if not cache.get(pv_key):
        increase_post_view = True
        cache.set(pv_key, 1, 2*60)

    if increase_post_view:
        Post.objects.filter(time_id=time_id).update(read_num=F('read_num') + 1)
