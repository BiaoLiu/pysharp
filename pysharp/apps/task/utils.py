# coding=utf-8

import time
import json
from pysharp.libs.common.log import logger
from celery import task, chain
from djcelery.models import PeriodicTask

from .models import Peroid_task_record
from .decorators import db_operator

# 周期性任务import包
#from celery.schedules import crontab
#from celery.task import periodic_task

#===============================================================================
# 周期性任务的路径
TASK = 'test_celery.utils.add' 
#===============================================================================


@task() 
#@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def add(x, y):
    """
    @summary: celery 示例任务
    @note: @periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))：每5分钟执行1次任务
              periodic_task 装饰器程序运行时自定触发定时任务
    """
    sums = x +y
    # 以下操作是保存任务的执行记录
    # 查询任务的对应的周期任务
    try:
        task = TASK
        args = [x,y]
        args = json.dumps(args)
        periodic_task = PeriodicTask.objects.filter(task=task, args=args)[0]
        periodic_task_id = periodic_task.id
    except:
        logger.error(u"查询任务的对应的周期任务出错")
        periodic_task_id = 0
    # 将执行记录保存到数据库中 
    try:
        excute_param = "x:%s, y:%s" % (x, y)
        Peroid_task_record.objects.create(
                                          excute_param=excute_param,
                                          excute_result=sums,
                                          periodic_task_id = periodic_task_id
                                          )
    except:
        logger.error(u"保存周期性任务执行记录出错")
    return sums


@task()  
def send_msg(username, title, **kwargs):   
    """
    @summary: 发送rtx
    """
    message = kwargs.get('message')
    schedule_time = kwargs.get('schedule_time')
    if schedule_time:
        msg = u"定时时间：%s\n消息：%s" % (schedule_time, message)
    else:
        msg = u"消息：%s" % message
    # res = send(username, username, title, msg)
    return None
            
            
def get_peroid_task_detail(task_id):
    """
    @summary: 查询周期任务和相关参数
    @param task_id:  周期任务id
    @return: {
           'task_args': 任务args参数,
           'task_kwargs': 任务kwargs参数,
           'cron_schedule':CrontabSchedule
           }
    """
    #  查询周期任务的信息
    try:
        period_task = PeriodicTask.objects.get(id=task_id)
        task = period_task.task
        task_args =  period_task.args   
        task_kwargs = period_task.kwargs 
        cron_schedule = period_task.crontab   # 周期时间参数
    except:
        task = TASK
        task_args = '[]'
        task_kwargs = '{}'
        cron_schedule = None 
    task_info = {
           'task_id': task_id,
           'task': task,
           'task_args': task_args,
           'task_kwargs': task_kwargs,
           'cron_schedule':cron_schedule
           }
    return task_info



@task() 
@db_operator('custom_func1')
def custom_func1(**kwargs):
    """
    @summary: 自定义函数1，可以自定义自己的逻辑处理
    """
    # 获取参数
    uin = kwargs.get('uin', '')
    param1 = kwargs.get('param1', '')
    # 处理逻辑
    message = u"自定义函数——参数1为：%s" % (param1)
    # 休眠10秒
    time.sleep(10)
    #返回参数
    result = True
    ret_msg = {
               'param1': param1,
               'message': message,
               }
    return {'result':result, 'ret_msg':ret_msg}
    
    
@task()  
@db_operator('custom_func2')
def custom_func2(fun_info, **kwargs):
    """
    @summary: 自定义函数2，可以自定义自己的逻辑处理
    """
    # 获取参数
    uin = kwargs.get('uin', '')
    param2 = kwargs.get('param2', '')
    # 处理逻辑
    message = u"自定义函数——参数2为：%s" % (param2)
    # 休眠5秒
    time.sleep(5)
    #返回参数
    result = True
    ret_msg = {
               'param2': param2,
               'message': message,
               }
    return {'result':result, 'ret_msg':ret_msg}


@task()  
@db_operator('custom_func3')
def custom_func3(fun_info, **kwargs):
    """
    @summary: 自定义函数3，可以自定义自己的逻辑处理
    """
    # 获取参数
    uin = kwargs.get('uin', '')
    param3 = kwargs.get('param3', '')
    # 处理逻辑
    message = u"自定义函数——参数3为：%s" % (param3)
    # 休眠5秒
    time.sleep(5)
    #返回参数
    result = True
    ret_msg = {
               'param2': param3,
               'message': message,
               }
    return {'result':result, 'ret_msg':ret_msg}
  
        
@task        
def chain_task(func1_param, func2_param, func3_param):
    """
    串行任务
    """
    chain(
        custom_func1.s( **func1_param),
        custom_func2.s(**func2_param),        
        custom_func3.s(**func3_param),
    ).apply_async()


def celery_chain_task(username, task_id, schedule_time, params):
    """
    @summary: celery串行执行任务
    @note: 
    后台任务：chain_task.delay(参数)
    后台定时任务：chain_task.apply_async((参数), eta=定时时间)
    调用celery任务方法详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    func1_param = params.get('custom_func1', {})
    func2_param = params.get('custom_func2', {})
    func3_param = params.get('custom_func3', {})
    # 自定义函数参数1
    func1_param['uin'] = username
    func1_param['task_id'] = task_id
    # 自定义函数参数2
    func2_param['uin'] = username
    func2_param['task_id'] = task_id
    # 自定义函数参数2
    func3_param['uin'] = username
    func3_param['task_id'] = task_id
    # 将任务串行起来，前面任务的返回可以作为后一个任务的参数
    if schedule_time:
        chain_task.apply_async((func1_param, func2_param, func3_param), eta=schedule_time) 
    else:
        chain_task.delay(func1_param, func2_param, func3_param)
    return (True, u"任务创建成功，正在后台执行")