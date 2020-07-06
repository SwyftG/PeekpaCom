import ssl
import pymongo
from django.views.generic import View
from django.shortcuts import render
from .decorators import peekpa_code_required
from django.utils.decorators import method_decorator
from apps.base.tracking_view import peekpa_tracking
from django.core.paginator import Paginator


@method_decorator(peekpa_code_required, name='get')
@method_decorator(peekpa_tracking, name='get')
class JpEarthView(View):

    client = pymongo.MongoClient("mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client['PeekpaMongoData']
    collection = db['JpEarth']

    def get(self, request):
        page = int(request.GET.get('p', 1))
        list_data = self.collection.find()
        paginator = Paginator(list(list_data), 15)
        page_obj = paginator.page(page)
        context = {
            "list_data": page_obj.object_list,
        }
        context.update(self.get_pagination_data(paginator, page_obj))
        return render(request, 'datacenter/jpearth/manage.html', context=context);

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 15:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

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

