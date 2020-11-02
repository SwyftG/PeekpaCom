from django.conf import settings
from django.core.paginator import Paginator


def get_pagination_data(paginator, page_obj,  around_count=2, list_type=False):
    current_page = page_obj.number
    num_pages = paginator.num_pages

    left_has_more = False
    right_has_more = False

    if current_page <= around_count + settings.ONE_PAGE_NEWS_COUNT:
        left_pages = list(range(1, current_page))
    else:
        left_has_more = True
        left_pages = list(range(current_page - around_count, current_page))

    if current_page >= num_pages - around_count - 1:
        right_pages = list(range(current_page + 1, num_pages + 1))
    else:
        right_has_more = True
        right_pages = list(range(current_page + 1, current_page + around_count + 1))
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


def get_paginator(data, number=settings.ONE_PAGE_NEWS_COUNT):
    return Paginator(data, number)