# coding:utf-8
from django.db import models
from django.contrib.auth.models import Group, AbstractUser, User
from django.conf import settings



class AppCompany(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    companyname = models.CharField(u'公司名称', max_length=200, blank=True, null=True)
    province = models.CharField(u'省', max_length=50, blank=True, null=True)
    city = models.CharField(u'市', max_length=50, blank=True, null=True)
    people_num = models.IntegerField(u'公司人数', blank=True, null=True)
    remark = models.TextField(u'备注', blank=True, null=True)

    class Meta:
        verbose_name = u"公司"
        verbose_name_plural = verbose_name
        db_table = u'app_company'


