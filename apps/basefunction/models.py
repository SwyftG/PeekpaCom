import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class NavbarItem(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    SHOW_PAGE_HOMEPAGE = 0
    SHOW_PAGE_CMS = 1
    SHOW_PAGE_FORUM = 2
    SHOW_PAGE_ITEMS = (
        (SHOW_PAGE_HOMEPAGE, '首页'),
        (SHOW_PAGE_CMS, 'CMS'),
        (SHOW_PAGE_FORUM, '论坛'),
    )
    name = models.CharField(max_length=30)
    show_name = models.CharField(max_length=30)
    url_path = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    show_page = models.PositiveIntegerField(default=SHOW_PAGE_HOMEPAGE, choices=SHOW_PAGE_ITEMS)
    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)

    def save(self, *args, **kwargs):
        if self.show_name:
            self.show_name = self.show_name
        else:
            self.show_name = self.name
        super().save(*args, **kwargs)


class UserIP(models.Model):
    ip_address = models.CharField(max_length=30)
    ip_location = models.CharField(max_length=30)
    end_point = models.CharField(default='/', max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    day = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-create_time']


class VisitNumber(models.Model):
    count = models.IntegerField(default=0)


class DayNumber(models.Model):
    day = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)


class FeaturePost(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    url_path = models.CharField(max_length=100, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS)