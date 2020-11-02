# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/1 11:15 AM'

from rest_framework import serializers
from .models import NavbarItem


class NavbarItemSerializer(serializers.ModelSerializer):
    count_number = serializers.IntegerField(allow_null=True)
    class Meta:
        model = NavbarItem
        fields = ('name', 'show_name', 'url_path', 'create_time', 'show_page', 'status', 'count_number')