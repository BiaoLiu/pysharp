# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),

    url(r'^authcallback/$',views.auth_callback)
]
