# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-24 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20170224_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celery_task',
            name='status',
            field=models.CharField(choices=[('2', '执行成功'), ('3', '执行失败'), ('0', '等待执行'), ('1', '正在执行')], default='0', max_length=5, verbose_name='总任务状态'),
        ),
        migrations.AlterField(
            model_name='task_node',
            name='status',
            field=models.CharField(choices=[('2', '执行成功'), ('3', '执行失败'), ('0', '等待执行'), ('1', '正在执行')], default='0', max_length=5, verbose_name='任务状态'),
        ),
    ]