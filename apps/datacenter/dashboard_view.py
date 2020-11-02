import datetime
import ssl
import random
import pymongo
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.base.redis_cache import get_data_from_cache
from apps.basefunction.global_peekpa import peekpa_config
from apps.basefunction.models import NavbarItem
from .serializer import DmmItemSerializer


class CenterDashboard(APIView):
    ATLAS_MONGO_URL = "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority"
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # context = self.get_side_bar_view()
        from_cache, context = get_data_from_cache(None, self.get_content_update_info, 1 * 60 * 60, redis_key="dash_board_view")
        from_cache_2, top_data = get_data_from_cache(None, self.get_top_actress_info, 48 * 60 * 60, redis_key="top_actress")
        context['from_cache'] = from_cache
        context['today_day_time'] = datetime.datetime.now().strftime("%Y年%m月%d日")
        context['top_actresses'] = top_data
        return Response(data=context, status=200)

    def get_dashboard_view(self):
        from_cache, context = get_data_from_cache(None, self.get_content_update_info, 1 * 60 * 60, redis_key="daily_update_info")
        return context

    def get_top_actress_info(self):
        database = pymongo.MongoClient(self.ATLAS_MONGO_URL, ssl_cert_reqs=ssl.CERT_NONE)['Avgle']
        collection = database['dmm_data']
        data_list = collection.find().sort("video_publish_day", direction=pymongo.DESCENDING)
        result = dict()
        for item in data_list:
            actress_name = item['search_name']
            video_number = item['video_number']

            # item['url'] = "https://www.dmm.co.jp/mono/dvd/-/detail/=/cid={}/".format(video_number)
            # item['video_poster'] = "https://pics.dmm.co.jp/mono/movie/adult/{}/{}pl.jpg".format(video_number, video_number)
            # item['video_poster_sm'] = "https://pics.dmm.co.jp/mono/movie/adult/{}/{}ps.jpg".format(video_number, video_number)
            # if "bod" in item['url']:
            #     item['pre_video_url'] = "https://cc3001.dmm.co.jp/litevideo/freepv/{}/{}/{}/{}_dmb_w.mp4".format(video_number[0], video_number[0:3], video_number, video_number)
            # else:
            #     item['pre_video_url'] = "https://cc3001.dmm.co.jp/litevideo/freepv/{}/{}/{}/{}_mhb_w.mp4".format(video_number[0], video_number[0:3], video_number, video_number)
            video_screenshot_list = list()
            video_screenshot_list_sm = list()
            video_screenshot_count = item['video_screenshot_list']
            for i in range(1, video_screenshot_count + 1, 1):
                video_screenshot_list.append("https://pics.dmm.co.jp/digital/video/{}/{}jp-{}.jpg".format(video_number, video_number, i))
                video_screenshot_list_sm.append("https://pics.dmm.co.jp/digital/video/{}/{}-{}.jpg".format(video_number, video_number, i))
            item['video_screenshot_list'] = video_screenshot_list
            item['video_screenshot_list_sm'] = video_screenshot_list_sm

            if actress_name in result.keys():
                result[actress_name].append(DmmItemSerializer(item).data)
            else:
                actress_data_list = list()
                actress_data_list.append(DmmItemSerializer(item).data)
                result[actress_name] = actress_data_list

        context_list = list()
        for actress_name in result.keys():
            data_list = result[actress_name]
            item = dict()
            item['name'] = actress_name
            item['tab_id'] = "id" + str(random.randrange(9999, 100000, 1)) + "peekpa"
            item['data_list'] = data_list[:12]
            context_list.append(item)
        return context_list


    def get_caoliu_post_update(self):
        today_day_time = datetime.datetime.now().strftime("%Y-%m-%d")
        yesterday_day_time = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
        database = pymongo.MongoClient(self.ATLAS_MONGO_URL, ssl_cert_reqs=ssl.CERT_NONE)['SpiderReport']
        collection = database['caoliu']
        # collection_data_list = list(collection.find({'day_time': {'$in':[yesterday_day_time, today_day_time]}}, {'data_type': True, 'count': True, 'day_time': True}))
        from_cache, collection_data_list = get_data_from_cache(None, self.get_data_from_collection_by_time, 1 * 60 * 60, redis_key="caoliu_spider_update_data", collection=collection, yesterday_time=yesterday_day_time, today_time=today_day_time)
        yesterday_data_list = [0] * 6
        today_data_list = [0] * 6
        yesterday_data_list, yesterday_total_number = self.get_data_from_caoliu_collection_list(collection_data_list,
                                                                                           yesterday_data_list, yesterday_day_time)
        today_data_list, today_total_new_number = self.get_data_from_caoliu_collection_list(collection_data_list,
                                                                                       today_data_list, today_day_time)
        new_count_map = dict()
        new_count_map['7'] = today_data_list[0]
        new_count_map['2'] = today_data_list[1]
        new_count_map['15'] = today_data_list[2]
        new_count_map['4'] = today_data_list[3]
        new_count_map['26'] = today_data_list[4]
        new_count_map['25'] = today_data_list[5]
        new_count_map['total'] = today_total_new_number

        result = {
            "yesterday_caoliu_data_list": yesterday_data_list,
            "today_caoliu_data_list": today_data_list,
            "today_caoliu_total_new_number": today_total_new_number,
            "new_caoliu_count_map": new_count_map
        }
        return result

    def get_jav_post_update(self):
        today_day_time = datetime.datetime.now().strftime("%Y-%m-%d")
        yesterday_day_time = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
        database = pymongo.MongoClient(self.ATLAS_MONGO_URL, ssl_cert_reqs=ssl.CERT_NONE)['SpiderReport']
        collection = database['javpop']
        # collection_data_list = list(collection.find({'day_time': {'$in': [yesterday_day_time, today_day_time]}},
        #                                             {'data_type': True, 'count': True, 'day_time': True}))
        from_cache, collection_data_list = get_data_from_cache(None, self.get_data_from_collection_by_time, 1 * 60 * 60,
                                                   redis_key="javpop_spider_update_data", collection=collection,
                                                   yesterday_time=yesterday_day_time, today_time=today_day_time)
        yesterday_data_list = [0] * 3
        today_data_list = [0] * 3
        yesterday_data_list, yesterday_total_number = self.get_data_from_javpop_collection_list(collection_data_list,
                                                                                           yesterday_data_list, yesterday_day_time)
        today_data_list, today_total_new_number = self.get_data_from_javpop_collection_list(collection_data_list,
                                                                                       today_data_list, today_day_time)
        new_count_map = dict()
        new_count_map['1'] = today_data_list[0]
        new_count_map['2'] = today_data_list[1]
        new_count_map['3'] = today_data_list[2]
        new_count_map['total'] = today_total_new_number
        result = {
            "yesterday_javpop_data_list": yesterday_data_list,
            "today_javpop_data_list": today_data_list,
            "today_javpop_total_new_number": today_total_new_number,
            "new_javpop_count_map": new_count_map
        }
        return result

    def get_data_from_caoliu_collection_list(self, collection_list, data_list, day_time):
        total_number = 0
        collection_list.rewind()
        for item in collection_list:
            if item['day_time'] == day_time:
                total_number += item['count']
                if item['data_type'] == "7":
                    data_list[0] += item['count']
                elif item['data_type'] == "2":
                    data_list[1] += item['count']
                elif item['data_type'] == "15":
                    data_list[2] += item['count']
                elif item['data_type'] == "4":
                    data_list[3] += item['count']
                elif item['data_type'] == "26":
                    data_list[4] += item['count']
                elif item['data_type'] == "25":
                    data_list[5] += item['count']
        return data_list, total_number

    def get_data_from_javpop_collection_list(self, collection_list, data_list, day_time):
        total_number = 0
        collection_list.rewind()
        for item in collection_list:
            if item['day_time'] == day_time:
                if item['data_type'] == "idol":
                    data_list[0] += item['count']
                elif item['data_type'] == "censored":
                    data_list[1] += item['count']
                elif item['data_type'] == "uncensored":
                    data_list[2] += item['count']
                elif item['data_type'] == "all":
                    total_number += item['count']
        return data_list, total_number

    def get_data_from_collection_by_time(self, collection, yesterday_time, today_time):
        data_list = collection.find({'day_time': {'$in': [yesterday_time, today_time]}},
                                                    {'data_type': True, 'count': True, 'day_time': True})
        return data_list

    def get_navitem_from_mysql(self, show_page):
        return NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=show_page)

    def get_content_update_info(self):
        context = {}
        context.update(self.get_caoliu_post_update())
        context.update(self.get_jav_post_update())
        return context