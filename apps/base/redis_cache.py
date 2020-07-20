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