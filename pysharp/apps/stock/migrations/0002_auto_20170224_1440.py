# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-24 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appquestion',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='appquestion',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
