from django.urls import path
from . import views

app_name = "center"

urlpatterns = [
    path("code/", views.input_code_view, name="center_input_code"),
    path("validate/", views.validate_code, name="center_validate_code"),

    path("center/", views.center_home_view, name="center_center_home_view"),
]