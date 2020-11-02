import ssl
import datetime
import pymongo

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.base.redis_cache import get_data_from_cache
from apps.datacenter.serializers import JpEarthSerializer
from .serializer import CaoliuSerializer, JavItemSerializer, AvgleItemSerializer, NineoneItemSerializer
from apps.datacenter.models import CaoliuBase, JavItem
from urllib import parse
from django.conf import settings
from apps.base.page_partation import get_pagination_data, get_paginator

TYPE_DAILY = 1
TYPE_SEARCH = 2

FID_CAOLIU = 1
FID_JAVPOP = 2
FID_AVGLE = 3
FID_NINEONE = 4
FID_JPEARTCH = 5

def process_paramter(request):
    fid = request.GET.get('fid', CaoliuBase.JISHUTAOLUN_7)
    search_key = request.GET.get('search')
    day = request.GET.get('day', datetime.datetime.now().strftime('%Y-%m-%d')).replace('/','-')
    handle_type = TYPE_DAILY if search_key is None else TYPE_SEARCH
    return handle_type, fid, day, search_key


def check_fid(fid):
    if fid == "102" or fid == "104" or fid == "107" or fid == "115" or fid == "125" or fid == "126":
        return FID_CAOLIU
    elif fid == "201" or fid == "202" or fid == "203":
        return FID_JAVPOP
    elif fid == "301":
        return FID_AVGLE
    elif fid == "350":
        return FID_NINEONE
    elif fid == "900":
        return FID_JPEARTCH


class CenterView(APIView):
    renderer_classes = [JSONRenderer]
    TYPE_ALL = 1
    TYPE_SEARCH = 2
    DB_JPEARTH = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)['PeekpaMongoData']
    DB_CAOLIU = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)['DailyProject']
    DB_JAV = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)["JavPopTest2"]
    DB_AVGLE = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)["Avgle"]
    DB_NINEONE = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)["Avgle"]

    def get(self, request):
        page = int(request.GET.get('p', 1))
        handle_type, fid, day, search_key = process_paramter(request)

        print("handle_type:{}, fid: {}, day:{}, search_key:{}".format(handle_type, fid, day, search_key))
        # 封装置后的数据缓存数据处理方法在这里
        from_cache, list_data = get_data_from_cache(request, self.get_data_from_db, handle_type=handle_type, fid=fid,
                                                    day=day, search_key=search_key)
        return self.handle_data_by_fid(from_cache, list_data, handle_type, fid, day, search_key, page)


    def handle_data_by_fid(self, from_cache, list_data, handle_type, fid, day, search_key, page):
        if check_fid(fid) == FID_CAOLIU:
            paginator = get_paginator(list_data)
            page_obj = paginator.page(page)
            page_obj_has_previous = page_obj.has_previous()
            page_obj_previous_page_number = page_obj.previous_page_number() if page_obj_has_previous else 0
            page_obj_has_next = page_obj.has_next()
            page_obj_next_page_number = page_obj.next_page_number() if page_obj_has_next else page
            context = {
                "list_data": CaoliuSerializer(page_obj.object_list, many=True).data,
                "cur_fid": fid,
                "cur_fid_name": self.get_fid_name(fid),
                "select_time": day,
                "search_key": search_key,
                'page_obj_previous_page_number': page_obj_previous_page_number,
                'page_obj_has_previous': page_obj_has_previous,
                'page_obj_next_page_number': page_obj_next_page_number,
                'page_obj_has_next': page_obj_has_next,
                'from_cache': from_cache,
                'url_query': '&' + parse.urlencode({
                    'search': search_key or '',
                    'fid': fid or '',
                    'day': day or '',
                })
            }
            context.update(get_pagination_data(paginator, page_obj, True))
            return Response(data=context, status=200)
        elif check_fid(fid) == FID_JAVPOP:
            paginator = get_paginator(list_data)
            page_obj = paginator.page(page)
            page_obj_has_previous = page_obj.has_previous()
            page_obj_previous_page_number = page_obj.previous_page_number() if page_obj_has_previous else 0
            page_obj_has_next = page_obj.has_next()
            page_obj_next_page_number = page_obj.next_page_number() if page_obj_has_next else page
            context = {
                "list_data": JavItemSerializer(page_obj.object_list, many=True).data,
                "cur_fid": fid,
                "cur_fid_name": self.get_fid_name(fid),
                "select_time": day,
                "search_key": search_key,
                'page_obj_previous_page_number': page_obj_previous_page_number,
                'page_obj_has_previous': page_obj_has_previous,
                'page_obj_next_page_number': page_obj_next_page_number,
                'page_obj_has_next': page_obj_has_next,
                'from_cache': from_cache,
                'url_query': '&' + parse.urlencode({
                    'search': search_key or '',
                    'fid': fid or '',
                    'day': day or '',
                })
            }
            context.update(get_pagination_data(paginator, page_obj, True))
            return Response(data=context, status=200)
        elif check_fid(fid) == FID_AVGLE:
            update_time = self.get_hot_update_time(fid)
            context = {
                "list_data": AvgleItemSerializer(list_data, many=True).data,
                'from_cache': from_cache,
                'update_time': update_time,
                "cur_fid_name": self.get_fid_name(fid),
            }
            return Response(data=context, status=200)
        elif check_fid(fid) == FID_NINEONE:
            update_time = self.get_hot_update_time(fid)
            context = {
                "list_data": NineoneItemSerializer(list_data, many=True).data,
                'from_cache': from_cache,
                'update_time': update_time,
                "cur_fid_name": self.get_fid_name(fid),
            }
            return Response(data=context, status=200)
        elif check_fid(fid) == FID_JPEARTCH:
            paginator = get_paginator(list_data)
            page_obj = paginator.page(page)
            page_obj_has_previous = page_obj.has_previous()
            page_obj_previous_page_number = page_obj.previous_page_number() if page_obj_has_previous else 0
            page_obj_has_next = page_obj.has_next()
            page_obj_next_page_number = page_obj.next_page_number() if page_obj_has_next else page
            context = {
                "list_data": JpEarthSerializer(page_obj.object_list, many=True).data,
                "cur_fid": fid,
                "cur_fid_name": self.get_fid_name(fid),
                "select_time": day,
                "search_key": search_key,
                'page_obj_previous_page_number': page_obj_previous_page_number,
                'page_obj_has_previous': page_obj_has_previous,
                'page_obj_next_page_number': page_obj_next_page_number,
                'page_obj_has_next': page_obj_has_next,
                'from_cache': from_cache,
                'url_query': '&' + parse.urlencode({
                    'search': search_key or '',
                    'fid': fid or '',
                    'day': day or '',
                })
            }
            context.update(get_pagination_data(paginator, page_obj, True))
            return Response(data=context, status=200)
            #
            # paginator = Paginator(list(list_data), settings.ONE_PAGE_NEWS_COUNT)
            # page_obj = paginator.page(page)
            # print(page_obj.object_list[0])
            # context = {
            #     "list_data": JpEarthSerializer(page_obj.object_list, many=True).data,
            #     "from_cache": from_cache
            # }
            # context.update(self.get_pagination_data(paginator, page_obj))
            # return Response(data=context, status=200)

    def get_hot_update_time(self, fid):
        if check_fid(fid) == FID_AVGLE:
            result = self.DB_AVGLE['avgle_hot_count'].find(projection=['search_time']).sort(
                "_id", direction=pymongo.DESCENDING)[:1]
        elif check_fid(fid) == FID_NINEONE:
            result = self.DB_NINEONE['nineone_hot_count'].find(projection=['search_time']).sort(
                "_id", direction=pymongo.DESCENDING)[:1]
        time_list = result[0]['search_time'].split('-')
        return "{}年{}月{}日，{}时".format(time_list[0], time_list[1], time_list[2], time_list[3])

    def process_paramter(self, request):
        search_key = request.GET.get('search')
        handle_type = self.TYPE_ALL if search_key is None else self.TYPE_SEARCH
        return handle_type, search_key

    def get_fid_name(self, fid):
        if fid == "107":
            return "技术讨论"
        elif fid =="102":
            return "亚洲无码"
        elif fid =="115":
            return "亚洲有码"
        elif fid =="104":
            return "欧美专场"
        elif fid =="126":
            return "中文原创"
        elif fid =="125":
            return "国产原创"
        elif fid == "201":
            return "写真"
        elif fid =="202":
            return "艺术马赛克"
        elif fid =="203":
            return "原汁原味"
        elif fid =="301":
            return "Avgle"
        elif fid =="350":
            return "91Pron"
        else:
            return "什么都不是"

    def get_data_from_db(self, handle_type, fid, day, search_key):
        result = None
        if check_fid(fid) == FID_CAOLIU:
            if handle_type == TYPE_DAILY or (search_key == '' and day):
                if fid == CaoliuBase.YAZHOU_WUMA_2:
                    result = self.DB_CAOLIU['fid2'].find({"post_day_time": day})
                elif fid == CaoliuBase.OUMEI_4:
                    result = self.DB_CAOLIU['fid4'].find({"post_day_time": day})
                elif fid == CaoliuBase.JISHUTAOLUN_7:
                    result = self.DB_CAOLIU['fid7'].find({"post_day_time": day})
                elif fid == CaoliuBase.YAZHOU_YOUMA_15:
                    result = self.DB_CAOLIU['fid15'].find({"post_day_time": day})
                elif fid == CaoliuBase.CHUOCHAN_25:
                    result = self.DB_CAOLIU['fid25'].find({"post_day_time": day})
                elif fid == CaoliuBase.ZHONGWEN_YUANCHUANG_26:
                    result = self.DB_CAOLIU['fid26'].find({"post_day_time": day})
            elif handle_type == TYPE_SEARCH:
                query_set = [{"post_title": {'$regex': ".*" + search_key + ".*"}},
                             {"post_title": {'$regex': ".*" + search_key.lower() + ".*"}},
                             {"post_title": {'$regex': ".*" + search_key.upper() + ".*"}}]
                if fid == CaoliuBase.YAZHOU_WUMA_2:
                    result = self.DB_CAOLIU['fid2'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
                elif fid == CaoliuBase.OUMEI_4:
                    result = self.DB_CAOLIU['fid4'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
                elif fid == CaoliuBase.JISHUTAOLUN_7:
                    result = self.DB_CAOLIU['fid7'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
                elif fid == CaoliuBase.YAZHOU_YOUMA_15:
                    result = self.DB_CAOLIU['fid15'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
                elif fid == CaoliuBase.CHUOCHAN_25:
                    result = self.DB_CAOLIU['fid25'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
                elif fid == CaoliuBase.ZHONGWEN_YUANCHUANG_26:
                    result = self.DB_CAOLIU['fid26'].find({"$or": query_set}).sort('post_day_time', pymongo.DESCENDING)
        elif check_fid(fid) == FID_JAVPOP:
            if handle_type == TYPE_DAILY or (search_key == '' and day):
                if fid == JavItem.XIEZHEN_201:
                    result = self.DB_JAV['VideoInfoIdol'].find({"video_post_time": day})
                elif fid == JavItem.YOUMA_202:
                    result = self.DB_JAV['VideoInfoCensored'].find({"video_post_time": day})
                elif fid == JavItem.WUMA_203:
                    result = self.DB_JAV['VideoInfoUncensored'].find({"video_post_time": day})
            elif handle_type == TYPE_SEARCH:
                query_set = [{"video_num": {'$regex': ".*" + search_key.lower() + ".*"}},
                             {"video_num": {'$regex': ".*" + search_key.upper() + ".*"}},
                             {"video_title": {'$regex': ".*" + search_key + ".*"}}]
                result = self.DB_JAV['VideoInfo'].find({"$or": query_set}).sort('video_post_time', pymongo.DESCENDING)
        elif check_fid(fid) == FID_AVGLE:
            result = self.DB_AVGLE['avgle_hot'].find(
                projection=['title', 'video_url', 'preview_video_url', 'index']).sort(
                "index", direction=pymongo.ASCENDING)[:90]
        elif check_fid(fid) == FID_NINEONE:
            result = self.DB_NINEONE['nineone_hot'].find(
                projection=['title', 'video_url', 'preview_video_url'])
        elif check_fid(fid) == FID_JPEARTCH:
            if handle_type == self.TYPE_ALL:
                result = self.DB_JPEARTH['JpEarth'].find({}, {"_id": False})
            else:
                result = self.DB_JPEARTH['JpEarth'].find({"jp_location": {'$regex': ".*" + search_key + ".*"}})
        return list(result)


    def get_pagination_data(self, paginator, page_obj, around_count=2):
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