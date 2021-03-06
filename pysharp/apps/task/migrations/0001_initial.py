# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-24 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Celery_task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='任务名称')),
                ('status', models.CharField(choices=[('3', '执行失败'), ('0', '等待执行'), ('1', '正在执行'), ('2', '执行成功')], default='0', max_length=5, verbose_name='总任务状态')),
                ('creator', models.CharField(max_length=30, verbose_name='创建者')),
                ('schedule_time', models.DateTimeField(blank=True, null=True, verbose_name='任务定时时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务说明')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name_plural': 'celery 任务',
                'verbose_name': 'celery 任务',
            },
        ),
        migrations.CreateModel(
            name='Peroid_task_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excute_param', models.TextField(verbose_name='任务执行参数')),
                ('excute_result', models.TextField(verbose_name='任务执行结果')),
                ('excute_time', models.DateTimeField(auto_now_add=True, verbose_name='任务执行时间')),
                ('periodic_task_id', models.IntegerField(default=0, verbose_name='周期性任务的id')),
            ],
            options={
                'ordering': ['-excute_time'],
                'verbose_name_plural': '周期性任务执行记录',
                'verbose_name': '周期性任务执行记录',
            },
        ),
        migrations.CreateModel(
            name='Task_node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='节点定义名称')),
                ('show_name', models.CharField(max_length=100, verbose_name='节点显示名称')),
                ('order', models.IntegerField(verbose_name='节点顺序')),
                ('excute_time', models.DateTimeField(blank=True, null=True, verbose_name='执行时间')),
                ('schedule_time', models.DateTimeField(blank=True, null=True, verbose_name='任务定时时间')),
                ('status', models.CharField(choices=[('3', '执行失败'), ('0', '等待执行'), ('1', '正在执行'), ('2', '执行成功')], default='0', max_length=5, verbose_name='任务状态')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务说明')),
                ('celery_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Celery_task')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': '任务节点',
                'verbose_name': '任务节点',
            },
        ),
        migrations.AlterUniqueTogether(
            name='task_node',
            unique_together=set([('celery_task', 'name')]),
        ),
    ]
