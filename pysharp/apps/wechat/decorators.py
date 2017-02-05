# coding=utf-8

"""
装饰器
功能开关装饰器，function_check（功能开关检测）  
"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs
from pysharp.apps.app_control.utils import func_check
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

SITE_URL=''


#==============================================================================
# check_function装饰器：功能开关检测
#==============================================================================
def function_check(func_code):
    """
    Decorator for views that check function.
    @param func_code: 功能code
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, message = func_check(func_code)
            if _result == 0 or _result == 1:
                return view_func(request, *args, **kwargs)
            else:
                return _redirect_func_check_failed(request)
        return _wrapped_view
    return decorator


def _redirect_func_check_failed(request):
    '''跳转func check失败的提示页面'''
    url = SITE_URL + 'accounts/check_failed/?code=func_check'
    if request.is_ajax():
        # ajax跳转页面，需要借助settings.js实现页面跳转或redirect跳转。
        resp = HttpResponse(status=403, content=url)
        return resp
    else:
        # 非ajax请求，则直接跳转页面
        return redirect(url)
