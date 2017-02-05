# coding=utf-8
'''
celery 周期任务封装

'''

from djcelery.models import PeriodicTask, CrontabSchedule


def add_peroid_task(task, name=None, minute='*', hour='*', 
                    day_of_week='*', day_of_month='*', 
                    month_of_year='*', args="[]", kwargs="{}"):
    """
    @summary: 添加一个周期任务
    @param task: 该task任务的模块路径名, 例如celery_sample.crontab_task
    @param name: 用户定义的任务名称, 具有唯一性 
    @note: PeriodicTask有很多参数可以设置，这里只提供简单常用的
    """
    cron_param = {
        'minute': minute,
        'hour': hour,
        'day_of_week': day_of_week,
        'day_of_month': day_of_month,
        'month_of_year': month_of_year
    }
    if not name:
        name = task
    try:
        cron_schedule = CrontabSchedule.objects.get(**cron_param)
    except CrontabSchedule.DoesNotExist:
        cron_schedule = CrontabSchedule(**cron_param)
        cron_schedule.save() 
    try:
        PeriodicTask.objects.create(
            name=name,
            task=task,
            crontab=cron_schedule ,
            args=args,
            kwargs=kwargs,
        )
    except Exception as e:
        return False, '%s' % e
    else:
        return True, ''
    

def edit_peroid_task_by_name(name, minute='*', hour='*', 
                    day_of_week='*', day_of_month='*', 
                    month_of_year='*', args="[]", kwargs="{}"):
    """
    @summary: 更新一个周期任务
    @param name: 用户定义的任务名称, 具有唯一性
    """
    try:
        period_task = PeriodicTask.objects.get(name=name)
    except PeriodicTask.DoesNotExist:
        return False, 'PeriodicTask.DoesNotExist'
    cron_param = {
        'minute': minute,
        'hour': hour,
        'day_of_week': day_of_week,
        'day_of_month': day_of_month,
        'month_of_year': month_of_year
    }
    try:
        cron_schedule = CrontabSchedule.objects.get(**cron_param)
    except CrontabSchedule.DoesNotExist:
        cron_schedule = CrontabSchedule(**cron_param)
        cron_schedule.save() 
    period_task.crontab = cron_schedule 
    period_task.args = args 
    period_task.kwargs = kwargs 
    period_task.save()
    return True, ''


def edit_peroid_task_by_id(task_id, minute='*', hour='*', 
                    day_of_week='*', day_of_month='*', 
                    month_of_year='*', args="[]", kwargs="{}"):
    """
    @summary: 更新一个周期任务
    @param name: 用户定义的任务名称, 具有唯一性
    """
    try:
        period_task = PeriodicTask.objects.get(id=task_id)
    except PeriodicTask.DoesNotExist:
        return False, 'PeriodicTask.DoesNotExist'
    cron_param = {
        'minute': minute,
        'hour': hour,
        'day_of_week': day_of_week,
        'day_of_month': day_of_month,
        'month_of_year': month_of_year
    }
    try:
        cron_schedule = CrontabSchedule.objects.get(**cron_param)
    except CrontabSchedule.DoesNotExist:
        cron_schedule = CrontabSchedule(**cron_param)
        cron_schedule.save() 
    period_task.crontab = cron_schedule 
    period_task.args = args 
    period_task.kwargs = kwargs 
    period_task.save()
    return True, ''


def del_peroid_task_by_name(name):
    """
    @summary: 根据周期任务的name删除该任务
    @param name: 用户定义的任务名称, 具有唯一性
    """
    try:
        PeriodicTask.objects.filter(name=name).delete()
        return True, ''
    except Exception as e:
        return False, '%s' % e


def del_peroid_task_by_id(task_id):
    """
    @summary: 根据周期任务的id删除该任务
    @param task_id: PeriodicTask库中记录的id
    """
    try:
        PeriodicTask.objects.filter(id=task_id).delete()
        return True, ''
    except Exception as e:
        return False, '%s' % e
    
