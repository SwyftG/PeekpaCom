from django.db import models
from shortuuidfield import ShortUUIDField
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

