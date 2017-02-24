from django.db import models


# from DjangoUeditor.models import UEditorField


# Create your models here.


class AppCompany(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    companyname = models.CharField('公司名称', max_length=200, blank=True, null=True)
    province = models.CharField('省', max_length=50, blank=True, null=True)
    city = models.CharField('市', max_length=50, blank=True, null=True)
    people_num = models.IntegerField('公司人数', blank=True, null=True)
    remark = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name
        db_table = 'app_company'
