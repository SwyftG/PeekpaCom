from rest_framework import serializers
from .models import CaoliuItem, JavItem


class CaoliuSerializer(serializers.Serializer):
    block_id = serializers.CharField()
    post_id = serializers.CharField()
    post_title = serializers.CharField()
    post_time = serializers.CharField()
    post_url = serializers.CharField()
    post_part_url = serializers.CharField()
    post_day_time = serializers.CharField()
    post_author = serializers.CharField(allow_null=True)

    class Meta:
        model = CaoliuItem
        fields = ('block_id', 'post_id', 'post_title', 'post_time', 'post_url', 'post_part_url', 'post_day_time', 'post_author')



class JavItemSerializer(serializers.Serializer):
    video_num = serializers.CharField()
    video_title = serializers.CharField()
    video_status = serializers.CharField()
    video_poster_list = serializers.ListField()
    video_screenshot_list = serializers.ListField()
    video_tag_list = serializers.ListField()
    video_actress_list = serializers.ListField()
    video_length = serializers.CharField()
    video_brand = serializers.CharField()
    video_post_time = serializers.CharField()

    class Meta:
        model = JavItem
        fields = ('video_num', 'video_title', 'video_status', 'video_poster_list', 'video_screenshot_list', 'video_tag_list', 'video_actress_list', 'video_length', 'video_brand', 'video_post_time')


class AvgleItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    video_url = serializers.CharField()
    preview_video_url = serializers.CharField()
    index = serializers.CharField()


class NineoneItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    video_url = serializers.CharField()
    preview_video_url = serializers.CharField()


class DmmItemSerializer(serializers.Serializer):
    video_title = serializers.CharField()
    url = serializers.CharField()
    video_poster = serializers.CharField()
    video_poster_sm = serializers.CharField()
    # video_screenshot_list = serializers.ListField()
    # video_screenshot_list_sm = serializers.ListField()
    video_publish_day = serializers.CharField()
    video_number = serializers.CharField()
    pre_video_url = serializers.CharField()
    search_name = serializers.CharField()