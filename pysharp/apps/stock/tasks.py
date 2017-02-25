# coding:utf-8
from celery import task

# from task.celery import app

@task(name='add相加')
def add(x, y):
    return x + y


@task(name='add2相加')
def add2(x, y):
    return x + y

