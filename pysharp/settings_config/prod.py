# coding:utf-8
'''
@summary: 全局常量设置
'''

import os
from ..settings import RUN_MODE

DB_HOST = os.environ.get('DB_HOST', "")
DB_PORT = os.environ.get('DB_PORT', '')

# APP的url前缀, 不要修改. 如 "/your_app_code/", 在页面中使用
SITE_URL = os.environ.get("PY_SITE_URL", "/")

# logging目录
LOGGING_DIR_ENV = os.environ.get('PY_LOGGING_DIR', '/data/home/apps/logs/')

# 测试环境配置
if RUN_MODE == 'TEST':
    # 静态资源目录url
    REMOTE_STATIC_URL = os.environ.get("REMOTE_STATIC_URL", '/static_api/')


# 正式环境配置
elif RUN_MODE == 'PRODUCT':
    # 静态资源目录url
    REMOTE_STATIC_URL = os.environ.get("BK_REMOTE_STATIC_URL", '/static_api/')
