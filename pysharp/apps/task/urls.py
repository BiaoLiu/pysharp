# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),

    # 定时任务
    url(r'^timing_task/$', views.timing_task),
    url(r'^excute_task/$', views.excute_task),

    # 周期任务
    url(r'^periodic_task/$', views.periodic_task),
    url(r'^get_periodic_tasks/$', views.get_periodic_tasks),
    url(r'^periodic_task_edit/(?P<task_id>\d+)/', views.periodic_task_edit),
    url(r'^check_peroid_task/$', views.check_peroid_task),
    url(r'^save_task/$', views.save_task),
    url(r'^del_peroid_task/$', views.del_peroid_task),
    # 周期任务 执行记录
    url(r'^periodic_task_record/(?P<task_id>\d+)/$', views.periodic_task_record),
    url(r'^get_records/$', views.get_records),

    # 串行任务
    url(r'^chain_task/$', views.chain_task),
    url(r'^get_flowchart/$', views.get_flowchart),
    url(r'^excute_chain_task/$', views.excute_chain_task),
]
