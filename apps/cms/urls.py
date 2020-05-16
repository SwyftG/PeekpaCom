from django.urls import path
from . import views
from .category_view import CategoryView, CategoryEditView, CategoryDeleteView
from .tag_view import TagView, TagEditView, TagDeleteView
from .post_view import PostView, PostEditView, PostDeleteView


app_name = "cms"

urlpatterns = [
    path("", views.cms_login, name="index"),
    path("dashboard/", views.cms_dashboard, name="dashboard"),
    path("login/", views.cms_login, name="login"),
    path("dashboard/category/manage", views.category_manage_view, name="category_manage_view"),
    path("dashboard/category/publish", views.category_publish_view, name="category_publish_view"),
    path("dashboard/category/add", CategoryView.as_view(), name="category_add"),
    path("dashboard/category/edit", CategoryEditView.as_view(), name="category_edit"),
    path("dashboard/category/delete", CategoryDeleteView.as_view(), name="category_delete"),

    path("dashboard/tag/manage", views.tag_manage_view, name="tag_manage_view"),
    path("dashboard/tag/publish", views.tag_publish_view, name="tag_publish_view"),
    path("dashboard/tag/add", TagView.as_view(), name="tag_add"),
    path("dashboard/tag/edit", TagEditView.as_view(), name="tag_edit"),
    path("dashboard/tag/delete", TagDeleteView.as_view(), name="tag_delete"),

    path("dashboard/post/manage", views.post_manage_view, name="post_manage_view"),
    path("dashboard/post/publish", views.post_publish_view, name="post_publish_view"),
    path("dashboard/post/add", PostView.as_view(), name="post_add"),
    path("dashboard/post/edit", PostEditView.as_view(), name="post_edit"),
    path("dashboard/post/delete", PostDeleteView.as_view(), name="post_delete"),
]