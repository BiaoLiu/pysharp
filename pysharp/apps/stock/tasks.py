# coding:utf-8
from celery import task

# from task.celery import app

@task()
def add(x, y):
    return x + y


@task()
def add2(x, y):
    return x + y

