# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-24 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=100, verbose_name='接收者')),
                ('from_user', models.CharField(max_length=100, verbose_name='发送者')),
                ('msg_created_time', models.IntegerField(verbose_name='消息时间')),
                ('event', models.CharField(choices=[('normal', '普通'), ('subscribe', '订阅'), ('unsubscribe', '退订'), ('client', 'CLICK'), ('view', 'VIEW'), ('scan', 'SCAN')], max_length=50, verbose_name='事件')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '事件消息',
                'db_table': 'w_event',
                'verbose_name': '事件消息',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('response_data', models.TextField(blank=True)),
                ('success', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '公众号菜单',
                'db_table': 'w_menu',
                'verbose_name': '公众号菜单',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=100, verbose_name='接受者')),
                ('from_user', models.CharField(max_length=100, verbose_name='发送者')),
                ('msg_created_time', models.IntegerField(verbose_name='消息时间')),
                ('msg_id', models.IntegerField(verbose_name='MsgId')),
                ('body', models.TextField()),
                ('response_content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '用户消息',
                'db_table': 'w_message',
                'verbose_name': '用户消息',
            },
        ),
        migrations.CreateModel(
            name='ResponseMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('normal', '普通'), ('subscribe', '订阅'), ('unsubscribe', '退订'), ('client', 'CLICK'), ('view', 'VIEW'), ('scan', 'SCAN')], max_length=50, verbose_name='事件')),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '响应消息',
                'db_table': 'w_response_message',
                'verbose_name': '响应消息',
            },
        ),
    ]
