from django.db import models

# Create your models here.


class ExchangeLink(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    name = models.CharField(max_length=30)
    show_name = models.CharField(max_length=30)
    url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)

    def save(self, *args, **kwargs):
        if self.show_name:
            self.show_name = self.show_name
        else:
            self.show_name = self.name
        super().save(*args, **kwargs)