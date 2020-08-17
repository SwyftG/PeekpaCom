from rest_framework import serializers


class JpEarthSerializer(serializers.Serializer):
    jp_title = serializers.CharField(allow_null=True)
    jp_create_time = serializers.CharField(allow_null=True)
    jp_url = serializers.CharField(allow_null=True)
    jp_id = serializers.CharField(allow_null=True)
    jp_time_num = serializers.CharField(allow_null=True)
    jp_location_image_url = serializers.CharField(allow_null=True)
    jp_location = serializers.CharField(allow_null=True)
    jp_level = serializers.CharField(allow_null=True)
    jp_max_level = serializers.CharField(allow_null=True)
    jp_time_text = serializers.CharField(allow_null=True)
    jp_peekpa = serializers.CharField(allow_null=True)

