import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.base.redis_cache import get_data_from_cache
from apps.basefunction.models import NavbarItem
from apps.basefunction.serializers import NavbarItemSerializer
from .dashboard_view import CenterDashboard


class CenterSidebarView(APIView):
    ATLAS_MONGO_URL = "mongodb+srv://peekpa-user:peekpa2020@peekpa.ofyco.mongodb.net/Peekpa?retryWrites=true&w=majority"
    def get(self, request):
        context = self.get_side_bar_view()
        return Response(data=context, status=200)

    def get_side_bar_view(self):
        from_cache, context = get_data_from_cache(None, self.handle_side_bar_data, 2 * 60 * 60, redis_key="side_bar_data")
        context['from_cache'] = from_cache
        return context

    def handle_side_bar_data(self):
        from_cache, navitems_caoliu = get_data_from_cache(None, self.get_navitem_from_mysql, 1 * 60 * 60, redis_key="caoliu_navitem_list", show_page=NavbarItem.SHOW_PAGE_CAOLIU)
        from_cache, navitems_jav = get_data_from_cache(None, self.get_navitem_from_mysql, 1 * 60 * 60, redis_key="jav_navitem_list", show_page=NavbarItem.SHOW_PAGE_JAV)
        from_cache, navitems_avgle = get_data_from_cache(None, self.get_navitem_from_mysql, 1 * 60 * 60, redis_key="avgle_navitem_list", show_page=NavbarItem.SHOW_PAGE_AVGLE)
        from_cache, navitems_nineone = get_data_from_cache(None, self.get_navitem_from_mysql, 1 * 60 * 60, redis_key="nineone_navitem_list", show_page=NavbarItem.SHOW_PAGE_NINEONE)
        dashboard = CenterDashboard()
        context = dashboard.get_dashboard_view()
        if context['new_caoliu_count_map']:
            for item in navitems_caoliu:
                item.count_number = context['new_caoliu_count_map'][str(int(item.url_path[-3:]) % 100)]
        if context['new_javpop_count_map']:
            for item in navitems_jav:
                item.count_number = context['new_javpop_count_map'][str(int(item.url_path[-3:]) % 200)]
        result = {
            "today_day_time": datetime.datetime.now().strftime("%Y年%m月%d日"),
            "today_caoliu_total_new_number": context['today_caoliu_total_new_number'],
            "caoliu_nav_list": NavbarItemSerializer(navitems_caoliu, many=True).data,
            "today_javpop_total_new_number": context['today_javpop_total_new_number'],
            "jav_nav_list": NavbarItemSerializer(navitems_jav, many=True).data,
            "avgle_nav_list": NavbarItemSerializer(navitems_avgle, many=True).data,
            "nineone_nav_list": NavbarItemSerializer(navitems_nineone, many=True).data,
        }
        return result

    def get_navitem_from_mysql(self, show_page):
        return NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL, show_page=show_page)