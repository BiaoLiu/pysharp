# coding=utf-8
import time
import datetime
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pysharp.libs.common.mymako import  render_json
from pysharp.libs.common.log import logger

from .models import Peroid_task_record, Celery_task, Task_node
from .constant import NODE_STATUS
from .utils import celery_chain_task, get_peroid_task_detail
from djcelery.models import PeriodicTask
from pysharp.libs.common.celery_task import add_peroid_task, edit_peroid_task_by_id, del_peroid_task_by_id
from .utils import send_msg

SITE_URL = ''


# 周期性任务的路径
TASK = 'test_celery.utils.add'
# 串行任务列表
TASK_LIST = ['custom_func1', 'custom_func2', 'custom_func3']



def index(request):
    """
    首页展示
    """
    return HttpResponseRedirect(SITE_URL + '/test_celery/periodic_task/')


def timing_task(request):
    """
    定时任务
    """
    return render(request, '/task/timing_task.html')


def excute_task(request):
    """
    @summary: 执行任务
    @note: 调用celery任务方法:
                task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
                task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
                delay(): 简便方法，类似调用普通函数
                apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    username = request.user.username
    params = request.POST.get('params', {})
    try:
        params = json.loads(params)
        msg_param = params.get('send_msg', {})
    except:
        msg = u"参数解析出错"
        logger.error(msg)
        result = {'result': False, 'message': msg}
        return render_json(result)
    # 定时参数
    is_schedule = params.get('is_schedule', {})
    do_schedule = is_schedule.get('do_schedule', 0)
    schedule_time = is_schedule.get('schedule_time', '') if do_schedule else ''
    schedule_timestamp = ''
    # 定时时间格式化
    if schedule_time:
        try:
            schedule_timestamp = time.mktime(time.strptime(schedule_time, '%Y-%m-%d %H:%M'))
            schedule_time = datetime.datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
        except Exception as  e:
            msg = u"定时时间(%s)格式错误:%s" % (schedule_time, e)
            logger.error(msg)
            return render_json({'result': False, 'message': msg})
    # 任务执行参数
    title = "后台任务"
    msg_param['schedule_time'] = schedule_time
    # 执行 celery 任务
    if schedule_time:
        # 后台定时执行
        send_msg.apply_async(args=[username, title], kwargs=msg_param, eta=schedule_time)
    else:
        # 后台任务
        send_msg.delay(username, title, **msg_param)
    return render_json({'result': True, 'message': schedule_timestamp})


def periodic_task(request):
    """
    周期任务首页
    """
    return render(request,'task/periodic_task.html')


def get_periodic_tasks(request):
    """
    查询所有周期任务
    """
    # 每页记录数
    record_num = int(request.GET.get('pageSize'))
    # 页码
    page_index = int(request.GET.get('page'))
    # 分片起始位置
    start = (page_index - 1) * record_num
    # 分片结束位置
    end = start + record_num
    peroid_tasks = PeriodicTask.objects.filter(task=TASK)
    total = peroid_tasks.count()
    task_set = peroid_tasks[start:end]
    data_list = []
    for task in task_set:
        data_list.append({
            'id': task.id,
            'task': task.task,
            'args': task.args,
            'kwargs': task.kwargs,
            'crontab': str(task.crontab)
        })
    data = {'data_list': data_list, 'total': total}
    return render_json({'result': True, 'data': data})


def periodic_task_edit(request, task_id):
    """
    启动、编辑任务页面，显示任务详情
    @todo: 通过task_id获取任务
    """
    task_info = get_peroid_task_detail(task_id)
    # 解析任务参数
    task_args = task_info.get('task_args', [])
    # 解析任务参数
    try:
        task_args = json.loads(task_args)
        task_args1 = task_args[0]
        task_args2 = task_args[1] if len(task_args) > 1 else 0
    except:
        task_args1 = 0
        task_args2 = 0
    task_info['task_args1'] = task_args1
    task_info['task_args2'] = task_args2
    return render(request, '/test_celery/periodic_task_edit.html', task_info)


def check_peroid_task(requets):
    """
    检查任务参数是否已存在（相同任务，相同参数的周期任务只允许有一条记录）
    相同任务，相同参数、不同调度策略的任务可以通过crontab策略的配置合并为一个任务
    """
    task = requets.POST.get('task', TASK)
    task_args_old = requets.POST.get('task_args_old', '[]')
    task_args1 = requets.POST.get('task_args1', '')
    task_args2 = requets.POST.get('task_args2', '')
    flag = False
    message = ''
    # 任务参数
    try:
        task_args1 = int(task_args1)
        task_args2 = int(task_args2)
        task_args_list = [task_args1, task_args2]
        task_args = json.dumps(task_args_list)
    except:
        logger.error(u"解析任务参数出错, task_args1;%s, task_args2;%s" % (task_args1, task_args2))
    else:
        # 参数未改变，则不用检查
        if task_args_old == task_args:
            flag = True
        else:
            count = PeriodicTask.objects.filter(task=task, args=task_args).count()
            if count == 0:
                flag = True
    if not flag:
        message = "任务名为：%s\n任务参数为：X:%s,Y:%s\n的周期任务已存在！" % (task, task_args1, task_args2)
    return render_json({'result': flag, 'message': message})


def save_task(request):
    """
    创建/编辑周期性任务 并 运行
    """
    periodic_task_id = request.POST.get('periodic_task_id', '0')
    params = request.POST.get('params', {})
    try:
        params = json.loads(params)
        add_param = params.get('add_task', {})
    except:
        msg = u"参数解析出错"
        logger.error(msg)
        result = {'result': False, 'message': msg}
        return render_json(result)
    task_args1 = add_param.get('task_args1', '0')
    task_args2 = add_param.get('task_args2', '0')
    # 任务参数
    try:
        task_args1 = int(task_args1)
        task_args2 = int(task_args2)
        task_args_list = [task_args1, task_args2]
        task_args = json.dumps(task_args_list)
    except:
        task_args = '[0,0]'
        logger.error(u"解析任务参数出错")
    # 周期参数
    minute = add_param.get('minute', '*')
    hour = add_param.get('hour', '*')
    day_of_week = add_param.get('day_of_week', '*')
    day_of_month = add_param.get('day_of_month', '*')
    month_of_year = add_param.get('month_of_year', '*')
    # 创建周期任务时，任务名必须唯一
    now = int(time.time())
    task_name = "%s_%s" % (TASK, now)
    if periodic_task_id == '0':
        # 创建任务并运行
        res, msg = add_peroid_task(TASK, task_name, minute, hour,
                                   day_of_week, day_of_month,
                                   month_of_year, task_args)
    else:
        # 修改任务
        res, msg = edit_peroid_task_by_id(periodic_task_id, minute, hour,
                                          day_of_week, day_of_month,
                                          month_of_year, task_args)
    return render_json({'result': res, 'message': msg})


def del_peroid_task(request):
    """
    删除周期性任务
    """
    task_id = request.POST.get('id')
    res, msg = del_peroid_task_by_id(task_id)
    if res:
        msg = u"任务删除成功"
    return render_json({'result': res, 'message': msg})


def periodic_task_record(request, task_id):
    """
    显示周期性任务执行记录页面
    """
    #  查询周期任务的信息
    task_info = get_peroid_task_detail(task_id)
    return render(request, '/test_celery/periodic_task_record.html', task_info)


def get_records(request):
    """
    获取周期性任务执行记录
    @todo: 查找指定任务的执行记录
    """
    periodic_task_id = request.GET.get('periodic_task_id', '')
    # 每页记录数
    record_num = int(request.GET.get('pageSize'))
    # 页码
    page_index = int(request.GET.get('page'))
    # 分片起始位置
    start = (page_index - 1) * record_num
    # 分片结束位置
    end = start + record_num
    peroid_tasks = Peroid_task_record.objects.all()
    if periodic_task_id:
        peroid_tasks = peroid_tasks.filter(periodic_task_id=periodic_task_id)
    total = peroid_tasks.count()
    task_set = peroid_tasks[start:end]
    data_list = []
    for task in task_set:
        data_list.append({
            'id': task.id,
            'excute_time': task.excute_time.strftime('%Y-%m-%d %H:%M:%S') if task.excute_time else '--',
            'excute_result': task.excute_result,
            'excute_param': task.excute_param
        })
    data = {'data_list': data_list, 'total': total}
    return render_json({'result': True, 'data': data})



# 串行任务
def chain_task(request):
    """
    串行任务
    """
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render(request, '/task/chain_task.html', {'now': cur_time})


def get_flowchart(request):
    """
    查询任务流程，生成任务流程图
    """
    task_id = request.GET.get('task_id', '')
    try:
        c_task = Celery_task.objects.get(id=task_id)
        status = c_task.status
        schedule_time = c_task.schedule_time
        # 查询节点的任务信息
        task_nodes = Task_node.objects.filter(celery_task=c_task)
        node_num = task_nodes.count()
    except:
        status = '0'
        schedule_time = ''
        task_nodes = None
    rtx = {
        'status': status,
        'schedule_time': schedule_time,
        'task_nodes': task_nodes,
        'node_num': node_num,
        'status_dict': NODE_STATUS,
    }
    return render(request, '/task/flow_chart.part', rtx)


def excute_chain_task(request):
    """
    执行任务
    """
    # 用户的 QQ号 存储在 username字段
    uin = request.user.username if request.user else ''
    params = request.POST.get('params', {})
    if not uin:
        msg = u"用户信息获取失败"
        logger.error(msg)
        result = {'result': False, 'message': msg}
        return render_json(result)
    try:
        params = json.loads(params)
    except Exception as e:
        logger.error(u"参数解析出错:%s\nparams:%s" % (e, params))
        msg = u"参数解析出错"
        result = {'result': False, 'message': msg}
        return render_json(result)
    # 创建任务
    try:
        # 任务名称(默认为当前时间)
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_info = params.get('task_name', {})
        task_name = task_info.get('task_name', cur_time)
        task = Celery_task.objects.create(
            name=task_name,
            creator=uin,
        )
        # 定时参数
        is_schedule = task_info.get('is_schedule', {})
        do_schedule = is_schedule.get('do_schedule', 0)
        schedule_time = is_schedule.get('schedule_time', '') if do_schedule else ''
        # 定时时间格式化
        if schedule_time:
            try:
                schedule_time = datetime.datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
                task.schedule_time = schedule_time
                task.save()
            except Exception as e:
                msg = u"定时时间(%s)格式错误:%s" % (schedule_time, e)
                logger.error(msg)
                return render_json({'result': False, 'message': msg})
        task_id = task.id
        task_list = TASK_LIST
        for i, task_name in enumerate(task_list):
            show_name = params.get(task_name, {}).get('show_name', task_name)
            task_node = Task_node.objects.create(name=task_name, show_name=show_name, celery_task=task, order=i + 1)
    except Exception as  e:
        logger.error(u"任务创建失败 :%s" % e)
        msg = u"任务创建失败 "
        return render_json({'result': False, 'message': msg})
    else:
        try:
            # 将解析后的参数传给celery任务
            res, msg = celery_chain_task(uin, task_id, schedule_time, params)
            if res == True:
                msg = task_id
        except:
            res = False
            msg = u"Celey功能正在开发中，敬请期待"
        result = {'result': res, 'message': msg}
        return render_json(result)
