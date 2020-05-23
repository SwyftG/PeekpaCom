from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError('请传邮箱')
        if not username:
            raise ValueError('请传入用户名')
        if not password:
            raise ValueError('请传入密码')

        user = self.model(email=email, username=username, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(email, username, password, **kwargs)

    def create_superuser(self, email, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(email, username, password, **kwargs)


# super user: g@g.com Swyft 12341234
class User(AbstractBaseUser, PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    access_part = models.CharField(max_length=200)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


