import datetime
import ssl

import pymongo
from django.views.generic import View
from django.shortcuts import render

from apps.base.common_view import get_navbar_item_homepage
from apps.basefunction.decorators import peekpa_url_check
from .common_view import get_side_bar_view
from .decorators import peekpa_code_required
from django.utils.decorators import method_decorator
from apps.base.tracking_view import peekpa_tracking
from apps.base.redis_cache import get_data_from_cache

@method_decorator(peekpa_code_required, name='get')
@method_decorator(peekpa_tracking, name='get')
class AvgleView(View):

    def get(self, request):
        context = get_side_bar_view()
        return render(request, 'datacenter/video/manage.html', context=context)


@method_decorator(peekpa_tracking, name='get')
class AvgleIndexView(View):
    TYPE_DAILY = 1
    TYPE_SEARCH = 2
    DB = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)["Avgle"]

    def get(self, request):
        page = int(request.GET.get('p', 1))
        handle_type, fid, day, search_key = self.process_paramter(request)
        from_cache, list_data = get_data_from_cache(request, self.get_data_from_db, expire=60 * 60,
                                                    handle_type=handle_type, fid=fid, day=day, search_key=search_key)
        update_time = self.get_avgle_hot_update_time()
        context = {
            "list_data": list_data,
            'from_cache': from_cache,
            'update_time': update_time,
        }
        context.update(get_navbar_item_homepage())
        return render(request, 'jav/list.html', context=context)

    def get_avgle_hot_update_time(self):
        result = self.DB['avgle_hot_count'].find(projection=['search_time']).sort(
            "_id", direction=pymongo.DESCENDING)[:1]
        time_list = result[0]['search_time'].split('-')
        return "{}年{}月{}日，{}时".format(time_list[0], time_list[1], time_list[2], time_list[3])

    def get_data_from_db(self, handle_type, fid, day, search_key):
        result = self.DB['avgle_hot'].find(projection=['title', 'video_url', 'preview_video_url', 'index']).sort(
            "index", direction=pymongo.ASCENDING)[:90]
        return list(result)

    def process_paramter(self, request):
        fid = request.GET.get('fid', "301")
        search_key = request.GET.get('search')
        day = request.GET.get('day', datetime.datetime.now().strftime('%Y-%m-%d')).replace('/', '-')
        handle_type = self.TYPE_DAILY if search_key is None else self.TYPE_SEARCH
        return handle_type, fid, day, search_key
