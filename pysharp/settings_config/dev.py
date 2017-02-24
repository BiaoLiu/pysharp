# coding:utf-8
'''
@summary: 全局常量设置
用于本地开发环境
'''

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pysharp',
        'USER': 'root',
        'PASSWORD': 'liubiao123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

# ===============================================================================
# 系统配置
# ===============================================================================
# 静态资源地址：
REMOTE_STATIC_URL = 'http://test.com/static_api/'
