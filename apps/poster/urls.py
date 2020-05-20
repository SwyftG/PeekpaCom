from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("detail/<int:time_id>/", views.detail, name="detail"),
    path("list/", views.post_list_view, name="post_list"),
]