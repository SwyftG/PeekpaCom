import datetime

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse

from apps.poster.models import Category, Tag, Post
from apps.basefunction.models import VisitNumber, DayNumber, UserIP
from apps.exchangelink.models import ExchangeLink
from apps.basefunction.models import NavbarItem, FeaturePost
from apps.peekpauser.models import User
from apps.datacenter.models import Code, InputCode
from django.core.paginator import Paginator
from django.conf import settings
from apps.peekpauser.decorators import peekpa_login_required, peekpa_login_superuser
from apps.basefunction.global_peekpa import init_peekpa, get_peekpa_item
from django.conf import settings

# Create your views here.


def cms_login(request):
    return render(request, 'cms/login.html')


@peekpa_login_required
def cms_dashboard(request):
    init_peekpa()
    context = {
        'peekpa_config_code_list': get_peekpa_item("CODE"),
        'peekpa_config_navitem_list': get_peekpa_item("NAVITEM"),
        'list_data_show_page': NavbarItem.SHOW_PAGE_ITEMS,
        'peekpa_version': settings.PEEKPA_VERSION
    }
    context.update(get_dashboard_top_data())
    context.update(get_dashboard_visitor_chart())
    context.update(get_dashboard_visitor_ip_table(10))
    context.update(get_dashboard_post_view_table(10))
    return render(request, 'cms/home/home.html', context=context)


@peekpa_login_required
def category_manage_view(request):
    context = {
        "list_data": Category.objects.all()
    }
    return render(request, 'cms/category/manage.html', context=context)


@peekpa_login_required
def category_publish_view(request):
    return render(request, 'cms/category/publish.html')


@peekpa_login_required
def tag_manage_view(request):
    context = {
        "list_data": Tag.objects.all()
    }
    return render(request, 'cms/tag/manage.html', context=context)


@peekpa_login_required
def tag_publish_view(request):
    return render(request, 'cms/tag/publish.html')


@peekpa_login_required
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


@peekpa_login_required
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


@peekpa_login_required
def exchangelink_manage_view(request):
    context = {
        "list_data": ExchangeLink.objects.all(),
        'list_data_status': ExchangeLink.STATUS_ITEMS
    }
    return render(request, 'cms/exchangelink/manage.html', context=context)


@peekpa_login_required
def exchangelink_publish_view(request):
    context = {
        'list_data_status': ExchangeLink.STATUS_ITEMS
    }
    return render(request, 'cms/exchangelink/publish.html', context=context)


@peekpa_login_required
def navitem_manage_view(request):
    context = {
        "list_data": NavbarItem.objects.all(),
        'list_data_status': NavbarItem.STATUS_ITEMS,
        'list_data_show_page': NavbarItem.SHOW_PAGE_ITEMS,
    }
    return render(request, 'cms/navitem/manage.html', context=context)


@peekpa_login_required
def feature_manage_view(request):
    context = {
        "list_data": FeaturePost.objects.all(),
        'list_data_status': FeaturePost.STATUS_ITEMS,
    }
    return render(request, 'cms/feature/manage.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
def code_manage_view(request):
    context = {
        "list_data": Code.objects.all(),
        'list_data_status': Code.STATUS_ITEMS,
    }
    return render(request, 'cms/code/manage.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
def user_manage_view(request):
    context = {
        "list_data": User.objects.all(),
    }
    return render(request, 'cms/user/manage.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
def data_center_inputcode_manage_view(request):
    context = {
        "item_data": InputCode.objects.get_or_create(id=1)[0],
    }
    return render(request, 'cms/datacenter/input_code.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
@require_POST
def data_center_inputcode_modify_view(request):
    name = request.POST.get('name')
    InputCode.objects.filter(id=1).update(name=name)
    return redirect(reverse('cms:data_center_inputcode_manage_view'))


@peekpa_login_required
def monitor_userip_view(request):
    page = int(request.GET.get('p', 1))
    posts = UserIP.objects.all().order_by('-create_time')
    paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    page_obj = paginator.page(page)
    day_count = DayNumber.objects.filter(day=timezone.now().date())
    ip_count_num = day_count[0].count if day_count else 0

    context = {
        "list_data": page_obj.object_list,
        "day_time": timezone.now().date(),
        "ip_count_num": ip_count_num
    }
    context_data = get_pagination_data(paginator, page_obj)
    context.update(context_data)
    return render(request, 'cms/monitor/userip_manage.html', context=context)


@peekpa_login_required
def monitor_postview_view(request):
    page = int(request.GET.get('p', 1))
    posts = get_dashboard_post_view_table(-1)['post_view_table_list']
    paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    page_obj = paginator.page(page)
    context = {
        "list_data": page_obj.object_list,
    }
    context_data = get_pagination_data(paginator, page_obj)
    context.update(context_data)
    return render(request, 'cms/monitor/post_view_manage.html', context=context)


@peekpa_login_required
def navitem_publish_view(request):
    context = {
        'list_data_status': NavbarItem.STATUS_ITEMS,
        'list_data_show_page': NavbarItem.SHOW_PAGE_ITEMS,
    }
    return render(request, 'cms/navitem/publish.html', context=context)


@peekpa_login_required
def feature_publish_view(request):
    context = {
        'list_data_status': FeaturePost.STATUS_ITEMS,
    }
    return render(request, 'cms/feature/publish.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
def code_publish_view(request):
    context = {
        'list_data_status': Code.STATUS_ITEMS,
    }
    return render(request, 'cms/code/publish.html', context=context)


@peekpa_login_required
@peekpa_login_superuser
def user_publish_view(request):
    context = {

    }
    return render(request, 'cms/user/publish.html', context=context)


def get_dashboard_top_data():
    post_num = Post.objects.all().count()
    day_visit_ip_set = set()
    day_visit_ip_list = UserIP.objects.filter(day=timezone.now().date())
    if day_visit_ip_list:
        for user_ip_item in day_visit_ip_list:
            if user_ip_item.ip_address not in day_visit_ip_set:
                day_visit_ip_set.add(user_ip_item.ip_address)
    day_visit_ip_num = len(day_visit_ip_set)
    day_visit_num = DayNumber.objects.filter(day=timezone.now().date())[0].count
    total_visit_num = VisitNumber.objects.filter(id=1)[0].count
    context = {
        "post_num": post_num,
        "day_visit_ip_num": day_visit_ip_num,
        "day_visit_num": day_visit_num,
        "total_visit_num": total_visit_num
    }
    return context


def get_dashboard_visitor_ip_table(max_num):
    visitor_data = UserIP.objects.filter(day=timezone.now().date())
    if len(visitor_data):
        visitor_data = visitor_data[:max_num]
    context = {
        'visitor_data_list': visitor_data,
    }
    return context


def get_dashboard_visitor_chart():
    days_list = []
    visit_list = []
    max_num = 0
    week_total_num = 0
    for index in range(6, -1, -1):
        day, format_date = get_before_date(index)
        days_list.append(int(day))
        day_visit_num = 0
        daynumber_item = DayNumber.objects.filter(day=format_date)
        if daynumber_item:
            day_visit_num = daynumber_item[0].count
        visit_list.append(day_visit_num)
        week_total_num += day_visit_num
        max_num = day_visit_num if day_visit_num > max_num else max_num
    context = {
        'visit_week_total_number': day_visit_num,
        'date_time_list': days_list,
        'week_data_list': visit_list,
        'suggested_max': max_num
    }
    return context


def get_before_date(day):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-day)
    re_day = (today + offset).strftime("%d")
    re_date = (today + offset).strftime("%Y-%m-%d")
    return re_day, re_date


def get_dashboard_post_view_table(max_num):
    visitor_day_data = UserIP.objects.filter(day=timezone.now().date(), end_point__contains='/detail/')
    post_map = {}
    post_view_table_list = []
    if visitor_day_data:
        for item in visitor_day_data:
            post_id = item.end_point.split('/')[2]
            if post_id in post_map:
                post_map[post_id] += 1
            else:
                post_map[post_id] = 1
    if post_map:
        for key in post_map:
            key = key
            post_item = Post.objects.filter(time_id=key)
            if post_item:
                post_item[0].inscrease = post_map[key]
                post_view_table_list.append(post_item[0])
    if post_view_table_list:
        post_view_table_list.sort(key=lambda x: x.inscrease, reverse=True)
    if max_num > 0 and len(post_view_table_list) > max_num:
        post_view_table_list = post_view_table_list[:max_num]
    context = {
        'post_view_table_list': post_view_table_list,
    }
    return context

