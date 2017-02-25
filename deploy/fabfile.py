#coding:utf-8

from fabric.api import *

# env.hosts=['root@120.27.46.167']

def deploy():
    code_dir='/project/boai'

    with lcd(code_dir):
        print('拉取GitHub更新...')
        local('git pull')
        print('启动boai virtualenv...')
        local('source /project/virtualenv/boai/bin/activate')
        print('收集静态资源...')
        local('/project/virtualenv/boai/bin/python manage.py collectstatic')
        print('重启uwsgi服务...')
        local('uwsgi --reload boai.pid')
        print('执行完毕')