# coding=utf-8

from django.contrib import admin
from .models import Peroid_task_record, Celery_task, Task_node


admin.site.register(Peroid_task_record)
admin.site.register(Celery_task)
admin.site.register(Task_node)