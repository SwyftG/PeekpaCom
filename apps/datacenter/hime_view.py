import datetime
import random
import ssl
from urllib import parse

import pymongo
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings

from apps.base.common_view import get_navbar_item_homepage
from apps.base.page_partation import get_paginator, get_pagination_data
from apps.basefunction.decorators import peekpa_url_check
from .common_view import get_side_bar_view
from .decorators import peekpa_code_required
from django.utils.decorators import method_decorator
from apps.base.tracking_view import peekpa_tracking
from apps.base.redis_cache import get_data_from_cache


# @method_decorator(peekpa_url_check, name='get')
@method_decorator(peekpa_tracking, name='get')
class HimeView(View):

    VIDEO_URL_FORMAT = "https://storage.googleapis.com/hime-content/{}/video/{}/{}.mp4"
    AT_MONGODB_CLIENT = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    DB = AT_MONGODB_CLIENT['HimeChannel']

    def get(self, request):
        list_data = self.get_data_from_db()
        context = {
            "list_data": list_data,
        }
        return render(request, 'hime/list_hime.html', context=context)

    def get_data_from_db(self):
        db_result = self.DB['video_info'].aggregate([{"$sample": {"size": 32}}])
        result = list()
        for video in db_result:
            item = dict()
            item['preview_video_url'] = self.VIDEO_URL_FORMAT.format(video['girl_hash_id'], video['post_hash_id'], video['post_hash_id'])
            item['title'] = "{}".format(video['title'])
            item['video_url'] = self.VIDEO_URL_FORMAT.format(video['girl_hash_id'], video['post_hash_id'], video['post_hash_id'])
            item['girl_hash_id'] = video['girl_hash_id']
            # print(item['video_url'])
            result.append(item)
        random.shuffle(result)
        return result


@method_decorator(peekpa_tracking, name='get')
class HimeDetailView(View):

    VIDEO_URL_FORMAT = "https://storage.googleapis.com/hime-content/{}/video/{}/{}.mp4"
    AT_MONGODB_CLIENT = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    DB = AT_MONGODB_CLIENT['HimeChannel']

    def get(self, request, girl_id):
        page = int(request.GET.get('p', 1))
        from_cache, list_data = get_data_from_cache(request, self.get_data_from_db, expire=12 * 60 * 60,
                                                    redis_key="hime-girl-{}".format(girl_id), girl_id=girl_id)
        from_cache, girl_profile = get_data_from_cache(request, self.get_girl_profile_from_db, expire=12 * 60 * 60,
                                                    redis_key="hime-girl-profile-{}".format(girl_id), girl_id=girl_id)
        paginator = get_paginator(list_data,number=12)
        page_obj = paginator.page(page)

        context = {
            "list_data": page_obj.object_list,
            "total": len(list_data),
            "page_obj": page_obj,
            "girl_profile": girl_profile
        }
        context.update(get_pagination_data(paginator, page_obj))
        return render(request, 'hime/list_hime_detail.html', context=context)

    def get_data_from_db(self, girl_id):
        db_result = self.DB['video_info'].find({'girl_hash_id': girl_id})
        result = list()
        for video in db_result:
            item = dict()
            item['preview_video_url'] = self.VIDEO_URL_FORMAT.format(video['girl_hash_id'], video['post_hash_id'], video['post_hash_id'])
            item['title'] = "{}".format(video['title'])
            item['video_url'] = self.VIDEO_URL_FORMAT.format(video['girl_hash_id'], video['post_hash_id'], video['post_hash_id'])
            item['girl_hash_id'] = video['girl_hash_id']
            # print(item['video_url'])
            result.append(item)
        return result

    def get_girl_profile_from_db(self, girl_id):
        db_result = self.DB['girl_info_profile'].find({'girl_hash_id': girl_id})
        if db_result.count():
            return db_result[0]
        return None