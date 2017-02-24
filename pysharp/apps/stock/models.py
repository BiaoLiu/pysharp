from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

QUESTION_MODE = (
    ('onetoone', '一对一'),
    ('free', '免费提问')
)


class AppQuestion(models.Model):
    question_id = models.IntegerField('id', primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='提问者', blank=True, null=True)
    content = models.TextField('内容', null=True)
    question_mode = models.CharField('提问模式', choices=QUESTION_MODE, max_length=20, blank=True, null=True)
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回答者', related_name='respondent', blank=True,
                                   null=True)
    question_price = models.DecimalField('提问价格', max_digits=18, decimal_places=2, blank=True, null=True)
    listen_price = models.DecimalField('偷听价格', max_digits=18, decimal_places=2, blank=True, null=True)
    listen_num = models.IntegerField('偷听数', blank=True, null=True)
    like_num = models.IntegerField('点赞数', blank=True, null=True)
    comment_num = models.IntegerField('评论数', blank=True, null=True)
    status = models.IntegerField('提问状态', blank=True, null=True)
    createtime = models.DateTimeField('创建时间', null=True)
    updatetime = models.DateTimeField('更新时间', null=True)

    class Meta:
        db_table = 'app_question'
        verbose_name = '提问'
        verbose_name_plural = '提问管理'

    def __str__(self):
        return self.content[0:20]
