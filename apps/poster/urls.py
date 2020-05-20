from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:time_id>/", views.detail, name="detail"),
    path("list/", views.post_list_view, name="post_list"),
    # path("logout/", views.login_view, name="logout"),
    # path("img_captcha/", views.img_captcha, name="img_captcha"),
    # path("sms_captcha/", views.sms_captcha, name="sms_captcha"),
    # path("register/", views.register, name="register"),
]