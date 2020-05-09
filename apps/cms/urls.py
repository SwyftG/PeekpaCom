from django.urls import path
from . import views


app_name = "cms"

urlpatterns = [
    path("", views.cms_login, name="index"),
    path("dashboard/", views.cms_dashboard, name="dashboard"),
    path("login/", views.cms_login, name="login"),
]