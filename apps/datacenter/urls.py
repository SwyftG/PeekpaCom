from django.urls import path
from . import views
from .jpearth_view import JpEarthView, JpEarthSendView

app_name = "center"

urlpatterns = [
    path("code/", views.input_code_view, name="center_input_code"),
    path("validate/", views.validate_code, name="center_validate_code"),

    path("center/", views.center_home_view, name="center_center_home_view"),

    path('jpearth/', JpEarthView.as_view(), name="jpearth_list_view"),
    path('jpearth/Send/<str:jp_id>', JpEarthSendView.as_view(), name="jpearth_send_view"),
]