from django.core.cache import cache

ONE_HOUR = 1 * 60 * 60

def get_data_from_cache(request, page_func, expire=ONE_HOUR, redis_key=None,**kwargs):
    if not redis_key:
        redis_key = request.get_full_path()
    from_cache = False
    try:
        if cache.get(redis_key):
            list_data = cache.get(redis_key)
            from_cache = True
        else:
            list_data = page_func(**kwargs)
            cache.set(redis_key, list_data, expire)
    except:
        list_data = page_func(**kwargs)
    return from_cache, list_data


def get_cache_keys_object():
    cache_item_list = list()
    try:
        keys_list = cache.keys("*")
        for key in keys_list:
            ttl = cache.ttl(key)
            item = dict()
            item['key'] = key
            item['ttl'] = num_to_time(ttl)
            cache_item_list.append(item)
    except:
        pass
    return cache_item_list


def num_to_time(timestamp):
    if timestamp < 60:
        return '{}秒'.format(timestamp)
    elif timestamp >= 60 and timestamp < 60*60:
        minutes = int(timestamp / 60)
        seconds = int(timestamp % 60)
        return '{}分{}秒'.format(minutes, seconds)
    else:
        hours = int(timestamp / 60 / 60)
        minutes = int(timestamp % (60 * 60)/60)
        seconds = int(timestamp%60)
        return '{}小时{}分{}秒'.format(hours,minutes, seconds)
