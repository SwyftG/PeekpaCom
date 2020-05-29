from apps.poster.models import Post
from apps.exchangelink.models import ExchangeLink
from apps.basefunction.models import NavbarItem, FeaturePost


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


def get_navbar_item_homepage():
    navitem = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=NavbarItem.SHOW_PAGE_HOMEPAGE)
    context = {
        'navitem_list': navitem
    }
    return context


def get_feature_post_post():
    feature_post = FeaturePost.objects.filter(status=FeaturePost.STATUS_NORMAL).order_by('-create_time')
    if len(feature_post) > 5:
        feature_post = feature_post[:5]
    context = {
        'feature_post': feature_post
    }
    return context