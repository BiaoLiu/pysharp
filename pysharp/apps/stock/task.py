# coding:utf-8
from celery import task


# from task.celery import app



@task(name='相加的task')
def add(x, y):
    return x + y


@task(name='相加的task2')
def add2(x, y):
    return x + y


# @task
# def spider_wall():
#     keywords = ['太阳能', '光伏', '晶硅', '多晶硅', '硅片']
#
#     for item in keywords:
#         parser_page(item,1)
