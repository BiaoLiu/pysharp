# coding=utf-8

"""
celery任务相关装饰器
"""
import json
import datetime

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.
from django.utils.decorators import available_attrs

from pysharp.libs.common.log import logger
from .models import Celery_task, Task_node


def db_operator(node_name):
    """
   @summary:  数据库操作
   节点执行前，判断总任务状态为“等待执行”或者“正在执行”，则执行该节点
   节点执行后，更改相应节点的任务状态
   @param task_id: celery 任务id
   @param node_name: 当前节点名称
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(*args, **kwargs):
            task_id = kwargs.get('task_id', '')
            try:
                task = Celery_task.objects.get(id=task_id)
                creator = task.creator
                msg_methord = task.msg_methord
                status = task.status
            except:
                logger.error(u"获取任务（task_id:%s）状态出错" % task_id)
                status = '0'
            try:
                msg_methord = json.loads(msg_methord)
            except:
                msg_methord = ['mail']
            # 总任务状态为“等待执行”或者“正在执行”
            if status in ['0', '1']:
                # 更新当前节点状态为正在执行
                Task_node.objects.filter(celery_task__id=task_id, name=node_name).update(status='1')
                node_num = Task_node.objects.filter(celery_task__id=task_id).count()
                try:
                    # 判断当前任务是否为第一个任务
                    cur_order = Task_node.objects.get(celery_task__id=task_id, name=node_name).order
                except:
                    cur_order = 0
                # 第一个节点更新总任务状态
                if cur_order == 1:
                    Celery_task.objects.filter(id=task_id).update(status='1')
                # 执行当前节点
                res = view_func(*args, **kwargs)
                ret_msg = res.get('ret_msg', {})
                message = ret_msg.get('message', '')
                # 解析任务执行结果
                result = res.get('result', False)
                node_status = '2' if result else '3'
                # 节点执行后，更改节点状态
                Task_node.objects.filter(celery_task__id=task_id, name=node_name).update(
                                                                                         status=node_status, 
                                                                                         desc=message,
                                                                                         excute_time = datetime.datetime.now()
                                                                                         )
                # 节点执行失败，更新总任务状态 
                if node_status == '3':
                    Celery_task.objects.filter(id=task_id).update(status='3')
                elif cur_order == node_num:
                    # 最后一个节点执行成功，更新总任务状态
                    Celery_task.objects.filter(id=task_id).update(status='2')
                return ret_msg
            else:
                return None
            
        return _wrapped_view   
    return decorator


    
    