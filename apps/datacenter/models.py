from django.db import models
from shortuuidfield import ShortUUIDField
from mongoengine.document import Document
from mongoengine.fields import *
# Create your models here.


class Code(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    code = models.CharField(max_length=20)
    uid = ShortUUIDField(primary_key=True)
    session_uid = ShortUUIDField(auto_created=True)
    session_name = models.CharField(max_length=30)
    visit_num = models.PositiveIntegerField(default=0, auto_created=True)
    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)
    create_time = models.DateTimeField(auto_now_add=True)


class InputCode(models.Model):
    name = models.CharField(max_length=20)

class CaoliuItem(Document):
    block_id = StringField()
    post_id = StringField()
    post_title = StringField()
    post_time = StringField()
    post_url = StringField()
    post_part_url = StringField()
    post_day_time = StringField()
    post_author = StringField()

    def __str__(self):
        return "CaoItem: {}, {}".format(self.block_id, self.post_title)

class CaoliuBase(Document):
    YAZHOU_WUMA_2 = '102'
    OUMEI_4 = '104'
    JISHUTAOLUN_7 = '107'
    YAZHOU_YOUMA_15 = '115'
    CHUOCHAN_25 = '125'
    ZHONGWEN_YUANCHUANG_26 = '126'
    meta = {'abstract': True,
            'db_alias': 'DailyProject'}
    block_id = StringField()
    post_id = StringField()
    post_title = StringField()
    post_time = StringField()
    post_url = StringField()
    post_part_url = StringField()
    post_day_time = StringField()
    post_author = StringField()

    def __str__(self):
        return "block_id: {}, {}".format(self.block_id, self.post_title)

class JavItem(Document):
    ALL_200 = '200'
    XIEZHEN_201 = '201'
    YOUMA_202 = '202'
    WUMA_203 = '203'
    meta = {'collection': 'VideoInfo',
            'db_alias': 'JavPopTest'}
    video_num = StringField()
    video_title = StringField()
    video_status = StringField()
    video_poster_list = ListField()
    video_screenshot_list = ListField()
    video_tag_list = ListField()
    video_actress_list = ListField()
    video_length = StringField()
    video_brand = StringField()
    video_post_time = StringField()
    video_view_time = StringField()

    def __str__(self):
        return "JavItem: {}, {}".format(self.video_num, self.video_title)