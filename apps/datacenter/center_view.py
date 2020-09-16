import ssl

import pymongo
from django.utils.decorators import method_decorator

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.base.redis_cache import get_data_from_cache
from django.core.paginator import Paginator
from .serializers import JpEarthSerializer
from django.conf import settings


class CenterView(APIView):
    renderer_classes = [JSONRenderer]
    TYPE_ALL = 1
    TYPE_SEARCH = 2
    client = pymongo.MongoClient(
        "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client['PeekpaMongoData']
    collection = db['JpEarth']

    def get(self, request):
        page = int(request.GET.get('p', 1))
        handle_type, search_key = self.process_paramter(request)
        # list_data = self.get_data_from_db(handle_type, search_key)
        # 封装置后的数据缓存数据处理方法在这里
        from_cache, list_data = get_data_from_cache(request, self.get_data_from_db, handle_type=handle_type,
                                                    search_key=search_key)
        paginator = Paginator(list(list_data), settings.ONE_PAGE_NEWS_COUNT)
        page_obj = paginator.page(page)
        print(page_obj.object_list[0])
        context = {
            "list_data": JpEarthSerializer(page_obj.object_list, many=True).data,
            "from_cache": from_cache
        }
        context.update(self.get_pagination_data(paginator, page_obj))
        return Response(data=context, status=200)

    def process_paramter(self, request):
        search_key = request.GET.get('search')
        handle_type = self.TYPE_ALL if search_key is None else self.TYPE_SEARCH
        return handle_type, search_key

    def get_data_from_db(self, handle_type, search_key):
        if handle_type == self.TYPE_ALL:
            result = self.collection.find({}, {"_id": False})
        else:
            result = self.collection.find({"jp_location": {'$regex': ".*" + search_key + ".*"}})
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