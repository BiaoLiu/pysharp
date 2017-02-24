from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class AuthUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        '''创建user'''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=AuthUserManager.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        # 添加用户详细信息
        user_profile = AppUserProfile(user_id=user.id)
        user_profile.save()

        return user

    def create_superuser(self, email, username, password):
        '''创建超级管理员'''
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class AuthUser(AbstractUser):
    nickname = models.CharField('昵称', max_length=40, blank=True, null=True)
    mobile = models.CharField('手机', max_length=20, null=True)
    avatar = models.CharField('头像', max_length=200, default='')

    objects = AuthUserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = '用户管理'


class AppUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    realname = models.CharField(max_length=20, blank=True, null=True)
    provice = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'app_user_profile'


class AppPlatformUser(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=40, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=20, blank=True, null=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    unionid = models.CharField(max_length=200, blank=True, null=True)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    refresh_token = models.CharField(max_length=200, blank=True, null=True)
    expiretime = models.DateTimeField(blank=True, null=True)
    profileurl = models.CharField(max_length=200, blank=True, null=True)
    ts = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'app_platform_user'
