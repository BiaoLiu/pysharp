# coding:utf-8
import os
import raven

'''
@summary: 用户自定义全局常量设置
'''

# ===============================================================================
# 静态资源
# ===============================================================================
# 静态资源文件(js,css等）在APP上线更新后, 由于浏览器有缓存, 可能会造成没更新的情况.
# 所以在引用静态资源的地方，都把这个加上，如：<script src="/a.js?v=${STATIC_VERSION}"></script>；
# 如果静态资源修改了以后，上线前改这个版本号即可
STATIC_VERSION = 1.0

# ===============================================================================
# CELERY 配置
# ===============================================================================

# 使用密码的配置：redis://:liubiao123456@127.0.0.1:6379:6379/0
BROKER_URL = 'redis://127.0.0.1:6379/0'  # 消息代理
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'  # 任务结果存放在Redis
CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化格式
CELERY_RESULT_SERIALIZER = 'json'  # 任务结果格式
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间
CELERY_ACCEPT_CONTENT = ['json']  # 指定接受的内容类型

# 定时任务 数据库调度
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


# ===============================================================================
# SENTRY 配置
# ===============================================================================

RAVEN_CONFIG = {
    'dsn': 'https://c2361baf2a3c49fbb73c2bdc9014e090:988094e339114041995ee0d71b1bca0d@sentry.io/146798',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}


# 内网ip列表
INTERNAL_IPS = []

# ==============================================================================
# 中间件和应用
# ==============================================================================
# 自定义中间件
MIDDLEWARE_CLASSES_CUSTOM = [

]

# 自定义APP
INSTALLED_APPS_CUSTOM = [
    # add your app here...
    # Note: 请注意在第一次syncdb时不加自己的app

    'boai',
    'pysharp.apps.pymodel',
    'pysharp.apps.stock',
    'pysharp.apps.task',
    'pysharp.apps.wechat'
]

# 测试环境数据库设置
DATABASES_TEST = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'DB_NAME',
            'USER': 'DB_NAME',
            'PASSWORD': 'DB_PWD',
            'HOST': 'DB_HOST',
            'PORT': 'DB_PORT',
        }
}

# 正式环境数据库设置
DATABASES_PRODUCT = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_NAME',
        'PASSWORD': 'DB_PWD',
        'HOST': 'DB_HOST',
        'PORT': 'DB_PORT',
    }
}

# ===============================================================================
# 日志级别
# ===============================================================================
# 本地开发环境日志级别
LOG_LEVEL_DEVELOP = 'DEBUG'
# 测试环境日志级别
LOG_LEVEL_TEST = 'INFO'
# 正式环境日志级别
LOG_LEVEL_PRODUCT = 'ERROR'
