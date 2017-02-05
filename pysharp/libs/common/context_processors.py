# coding=utf-8
'''
context_processor for common(setting)

** 除setting外的其他context_processor内容，均采用组件的方式(string)
'''
from django.conf import settings


def mysetting(request):
    return {
            'MEDIA_URL': settings.MEDIA_URL,                              # MEDIA_URL
            'STATIC_URL': settings.STATIC_URL,                            # 本地静态文件访问
            'APP_PATH': request.get_full_path(),                          # 当前页面，主要为了login_required做跳转用
            'LOGIN_URL': '',                                              # 登录链接
            'LOGOUT_URL': '',                                             # 登出链接
            'RUN_MODE': settings.RUN_MODE,                                 # 运行模式
            'SITE_URL': settings.SITE_URL,                                 # URL前缀
            'REMOTE_STATIC_URL': settings.REMOTE_STATIC_URL,              # 远程静态资源url
            'STATIC_VERSION': settings.STATIC_VERSION,                    # 静态资源版本号,用于指示浏览器更新缓存
            'CHINESE_NAME': request.session.get('chinese_name', ''),     # 用户中文名
            }
