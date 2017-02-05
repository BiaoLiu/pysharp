# coding=utf-8

"""
装饰器
1.权限pad装饰器，permission_required
"""

from django.http import HttpResponseForbidden, HttpResponse
from django.utils.decorators import available_attrs
from .log import logger
from django.shortcuts import redirect
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

SITE_URL=''

#===============================================================================
# 转义装饰器
#===============================================================================
def escape_exempt(view_func):
    """
    转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)

def escape_script(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行javascript escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_script = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)

def escape_url(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行url escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_url = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


#==============================================================================
# 权限判断装饰器
#==============================================================================
# 判断当前登录用户是否 有指定业务的权限
def permission_required(app_code):
    """
    Decorator for views that checks whether a user has a particular permission
    to access the app_code, redirecting to the 403 page if necessary.
    Unused.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            username = request.user.username
            res = (username, )
            # TODO 调用判断权限的方法
            if res:
                return view_func(request, *args, **kwargs)
            # 权限不足提示页面，可根据实际情况修改
            return _redirect_403(request)

        return _wrapped_view
    return decorator


def _response_for_failure(request, _result, message, is_ajax):
    '''
    内部通用方法: 请求敏感权限出错时的处理(1和2)
    @param _result: 结果标志位
    @param message: 结果信息
    @param is_ajax: 是否是ajax请求
    '''
    if _result == 1:
        # 登陆失败，需要重新登录,跳转至登录页
        if is_ajax:
            return HttpResponse(status=402)
        return redirect(message)
    elif _result == 2:
        # error(包括exception)
        return _redirect_403(request)


def _redirect_403(request):
    '''转到403权限不足的提示页面'''
    url = SITE_URL + '/check_failed/?code=403'
    if request.is_ajax():
        resp = HttpResponse(status=403, content=url)
        return resp
    else:
        return redirect(url)

    
