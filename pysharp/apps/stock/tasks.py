# coding:utf-8
from celery import task


# from task.celery import app

@task()
def add(x, y):
    print('%s + %s 的结果：' % (x, y))
    return x + y


@task()
def add2(x, y):
    return x + y
