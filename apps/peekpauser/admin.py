from django.contrib import admin
from .models import User


class PeekpaUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, PeekpaUserAdmin)