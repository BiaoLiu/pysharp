#coding=utf-8

from django.db import models
from .constant import NODE_STATUS


class Peroid_task_record(models.Model):
    """
    周期性任务执行记录
    """
    excute_param = models.TextField("任务执行参数")
    excute_result = models.TextField("任务执行结果")
    excute_time = models.DateTimeField("任务执行时间", auto_now_add=True)
    periodic_task_id = models.IntegerField("周期性任务的id", default=0)
    
    def __str__(self):
        return '%s--%s--%s' % (self.periodic_task_id, self.excute_param, self.excute_time)
    
    class Meta:
        verbose_name = "周期性任务执行记录"
        verbose_name_plural = "周期性任务执行记录"
        ordering = ['-excute_time']
        
        
class Celery_task(models.Model):
    """
    celery 任务
    """
    name = models.CharField("任务名称", max_length=100)
    status = models.CharField("总任务状态", max_length=5, choices=[(st, NODE_STATUS[st]) for st in NODE_STATUS] ,default='0')
    creator = models.CharField("创建者", max_length=30)
    schedule_time = models.DateTimeField("任务定时时间", null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    desc = models.TextField("任务说明", null=True, blank=True )
    
    class Meta:
        verbose_name = "celery 任务"
        verbose_name_plural = "celery 任务"
        ordering = ['-create_time']
        
    def __str__(self):
        return  self.name
        
        
class Task_node(models.Model):
    """
    任务节点
    """
    celery_task = models.ForeignKey(Celery_task)
    name = models.CharField("节点定义名称", max_length=100)
    show_name = models.CharField("节点显示名称", max_length=100)
    order = models.IntegerField("节点顺序")
    excute_time = models.DateTimeField("执行时间", null=True, blank=True )
    schedule_time = models.DateTimeField("任务定时时间", null=True, blank=True)
    status = models.CharField("任务状态", max_length=5, choices=[(st, NODE_STATUS[st]) for st in NODE_STATUS] ,default='0')
    desc = models.TextField("任务说明", null=True, blank=True )
    
    class Meta:
        verbose_name = "任务节点"
        verbose_name_plural = "任务节点"
        unique_together = ('celery_task', 'name')
        ordering = ['order']
        
    def __str__(self):
        return  "%s--%s" % ( self.celery_task.name, self.name)    
    
    