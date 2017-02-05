# coding:utf-8
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


#===============================================================================
# CELERY 配置
#===============================================================================
# APP是否使用celery
IS_USE_CELERY = True           # APP 中 使用 celery 时，将该字段设为 True
# TOCHANGE调用celery任务的文件路径, 即包含如下语句的文件： from celery import task
# CELERY_IMPORTS = (
#                   'test_celery.utils',
#                   )


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

    'pysharp.apps.boai_admin',
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
