import datetime
import ssl

import pymongo

from apps.basefunction.models import NavbarItem
from django.conf import settings
from apps.base.redis_cache import get_data_from_cache


def get_side_bar_view():
    from_cache, context = get_data_from_cache(None, handle_side_bar_data, 2 * 60 * 60, redis_key="side_bar_data")
    return context

def handle_side_bar_data():
    context = {}
    navitems_caoliu = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=NavbarItem.SHOW_PAGE_CAOLIU)
    navitems_jav = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=NavbarItem.SHOW_PAGE_JAV)
    navitems_avgle = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=NavbarItem.SHOW_PAGE_AVGLE)
    navitems_nineone = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=NavbarItem.SHOW_PAGE_NINEONE)
    context.update(get_caoliu_post_update())
    context.update(get_jav_post_update())
    if context['new_caoliu_count_map']:
        for item in navitems_caoliu:
            item.count_number = context['new_caoliu_count_map'][str(int(item.url_path[-3:]) % 100)]
    if context['new_javpop_count_map']:
        for item in navitems_jav:
            item.count_number = context['new_javpop_count_map'][str(int(item.url_path[-3:]) % 200)]
    context.update({
        "caoliu_nav_list": navitems_caoliu,
        "jav_nav_list": navitems_jav,
        "avgle_nav_list": navitems_avgle,
        "nineone_nav_list": navitems_nineone,
    })
    return context

def get_caoliu_post_update():
    today_day_time = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday_day_time = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    database = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)['SpiderReport']
    collection = database['caoliu']
    yesterday_collection_list = list(collection.find({'day_time': yesterday_day_time}))
    today_collection_list = list(collection.find({'day_time': today_day_time}))

    yesterday_data_list = [0] * 6
    today_data_list = [0] * 6
    yesterday_data_list, yesterday_total_number = get_data_from_caoliu_collection_list(yesterday_collection_list, yesterday_data_list)
    today_data_list, today_total_new_number = get_data_from_caoliu_collection_list(today_collection_list, today_data_list)
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


def get_jav_post_update():
    today_day_time = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday_day_time = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    database =  pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)['SpiderReport']
    collection = database['javpop']
    yesterday_collection_list = list(collection.find({'day_time': yesterday_day_time}))
    today_collection_list = list(collection.find({'day_time': today_day_time}))
    yesterday_data_list = [0] * 3
    today_data_list = [0] * 3
    yesterday_data_list, yesterday_total_number = get_data_from_javpop_collection_list(yesterday_collection_list, yesterday_data_list)
    today_data_list, today_total_new_number = get_data_from_javpop_collection_list(today_collection_list, today_data_list)
    new_count_map = dict()
    new_count_map['1'] = today_data_list[0]
    new_count_map['2'] = today_data_list[1]
    new_count_map['3'] = today_data_list[2]
    new_count_map['total'] = today_total_new_number
    result = {
        "yesterday_javpop_data_list": yesterday_data_list,
        "today_javpop_data_list": today_data_list,
        "today_javpop_total_new_number": today_total_new_number,
        "new_javpop_count_map":new_count_map
    }
    return result



def get_data_from_caoliu_collection_list(collection_list, data_list):
    total_number = 0
    for item in collection_list:
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


def get_data_from_javpop_collection_list(collection_list, data_list):
    total_number = 0
    for item in collection_list:
        if item['data_type'] == "idol":
            data_list[0] += item['count']
        elif item['data_type'] == "censored":
            data_list[1] += item['count']
        elif item['data_type'] == "uncensored":
            data_list[2] += item['count']
        elif item['data_type'] == "all":
            total_number += item['count']
    return data_list, total_number