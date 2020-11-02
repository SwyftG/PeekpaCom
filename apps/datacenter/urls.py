from django.urls import path
from . import views
from .jpearth_view import JpEarthView, JpEarthSendView
from .center_api_view import CenterApiView
from .center_view import CenterView
from .caoliu_view import CaoliuListView
from .javpop_view import JavPopView
from .avgle_view import AvgleView, AvgleIndexView
from .nineone_view import NineoneView
from .dashboard_view import CenterDashboard
from .hime_view import HimeView, HimeDetailView

app_name = "center"

urlpatterns = [
    path("code/", views.input_code_view, name="center_input_code"),
    path("validate/", views.validate_code, name="center_validate_code"),

    path("center/", views.center_home_view, name="center_center_home_view"),

    path('jpearth/', JpEarthView.as_view(), name="jpearth_list_view"),
    path('jpearth/Send/<str:jp_id>', JpEarthSendView.as_view(), name="jpearth_send_view"),

    # 第十讲的前后端分离
    path('center/data/', CenterView.as_view(), name="jpearth_view"),

    #第十一讲的Token验证
    path('api/center/data/', CenterApiView.as_view(), name="jpearth_api_view"),
    path("jav/", AvgleIndexView.as_view(), name="avgle_index_view"),

    path("hime/", HimeView.as_view(), name="hime_view"),
    path("hime/<str:girl_id>/", HimeDetailView.as_view(), name="hime_detail_view"),

    path("cl1024/", CaoliuListView.as_view(), name="caoliu_list_view"),
    path("javpop/", JavPopView.as_view(), name="javpop_view"),
    path("avgle/", AvgleView.as_view(), name="avgle_view"),
    path("91pron/", NineoneView.as_view(), name="nineone_view"),
    path("center/dashboard", CenterDashboard.as_view(), name="center_dashboard_view"),
]