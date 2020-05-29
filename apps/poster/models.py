from django.db import models
import datetime
import mistune

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey('peekpauser.User', on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField()

    content = models.TextField()
    content_html = models.TextField(blank=True, editable=False)
    is_md = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)

    priority = models.IntegerField(default=-1)
    is_hot = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_main_page = models.BooleanField(default=False)

    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)
    publish_time = models.DateTimeField(auto_now_add=True)
    publish_time_show = models.DateTimeField(default=datetime.datetime.now)
    time_id = models.CharField(blank=True, max_length=30)
    read_num = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-time_id']

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        if not self.time_id or len(self.time_id) == 0:
            self.time_id = self.publish_time_show.strftime("%Y%m%d%H%M")
        super().save(*args, **kwargs)