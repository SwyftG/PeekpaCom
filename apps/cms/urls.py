from django.urls import path
from . import views
from .category_view import CategoryView, CategoryEditView, CategoryDeleteView
from .tag_view import TagView, TagEditView, TagDeleteView
from .post_view import PostView, PostEditView, PostDeleteView
from .exchangelink_view import ExchangeLinkView, ExchangeLinkEditView, ExchangeLinkDeleteView
from .navitem_view import NavItemView, NavItemEditView, NavItemDeleteView
from .code_view import CodeView, CodeEditView, CodeDeleteView
from .user_view import UserView, UserDeleteView
from .feature_view import FeatureView, FeatureEditView, FeatureDeleteView


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

    path("dashboard/exchangelink/manage", views.exchangelink_manage_view, name="exchangelink_manage_view"),
    path("dashboard/exchangelink/publish", views.exchangelink_publish_view, name="exchangelink_publish_view"),
    path("dashboard/exchangelink/add", ExchangeLinkView.as_view(), name="exchangelink_add"),
    path("dashboard/exchangelink/edit", ExchangeLinkEditView.as_view(), name="exchangelink_edit"),
    path("dashboard/exchangelink/delete", ExchangeLinkDeleteView.as_view(), name="exchangelink_delete"),

    path("dashboard/navitem/manage", views.navitem_manage_view, name="navitem_manage_view"),
    path("dashboard/navitem/publish", views.navitem_publish_view, name="navitem_publish_view"),
    path("dashboard/navitem/add", NavItemView.as_view(), name="navitem_add"),
    path("dashboard/navitem/edit", NavItemEditView.as_view(), name="navitem_edit"),
    path("dashboard/navitem/delete", NavItemDeleteView.as_view(), name="navitem_delete"),

    path("dashboard/monitor/userip", views.monitor_userip_view, name="monitor_userip_view"),
    path("dashboard/monitor/postview", views.monitor_postview_view, name="monitor_postview_view"),

    path("dashboard/code/manage", views.code_manage_view, name="code_manage_view"),
    path("dashboard/code/publish", views.code_publish_view, name="code_publish_view"),
    path("dashboard/code/add", CodeView.as_view(), name="code_add"),
    path("dashboard/code/edit", CodeEditView.as_view(), name="code_edit"),
    path("dashboard/code/delete", CodeDeleteView.as_view(), name="code_delete"),

    path("dashboard/user/manage", views.user_manage_view, name="user_manage_view"),
    path("dashboard/user/publish", views.user_publish_view, name="user_publish_view"),
    path("dashboard/user/add", UserView.as_view(), name="user_add"),
    path("dashboard/user/delete", UserDeleteView.as_view(), name="user_delete"),

    path("dashboard/inputcode/manage", views.data_center_inputcode_manage_view, name="data_center_inputcode_manage_view"),
    path("dashboard/inputcode/modify", views.data_center_inputcode_modify_view, name="data_center_inputcode_modify"),

    path("dashboard/feature/manage", views.feature_manage_view, name="feature_manage_view"),
    path("dashboard/feature/publish", views.feature_publish_view, name="feature_publish_view"),
    path("dashboard/feature/add", FeatureView.as_view(), name="feature_add"),
    path("dashboard/feature/edit", FeatureEditView.as_view(), name="feature_edit"),
    path("dashboard/feature/delete", FeatureDeleteView.as_view(), name="feature_delete"),
]