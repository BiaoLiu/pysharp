# coding=utf-8
import re
import json
from django.conf import settings
# from settings import SITE_URL
from django.views.debug import technical_500_response
import sys

from .log import logger
from .utils import html_escape, url_escape, html_escape_name, check_script


class CheckXssMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        try:
            # 判断豁免权
            if getattr(view, 'escape_exempt', False):
                return None

            escapeType = None
            if getattr(view, 'escape_script', False):
                escapeType = "script"
            elif getattr(view, 'escape_url', False):
                escapeType = "url"
            # get参数转换
            request.GET = self.__escape_data(request.path, request.GET, escapeType)
            # post参数转换
            request.POST = self.__escape_data(request.path, request.POST, escapeType)
        except Exception as e:
            logger.error(u"CheckXssMiddleware 转换失败！%s" % e)
        return None

    def __escape_data(self, path, query_dict, escape_type=None):
        """
        GET/POST参数转义
        """
        data_copy = query_dict.copy()
        new_data = {}
        for _get_key, _get_value in data_copy.items():
            # json串不进行转义
            try:
                to_json = json.loads(_get_value)
                is_json = True
            except Exception as e:
                is_json = False
            # 转义新数据
            if not is_json:
                try:
                    if escape_type == None:
                        use_type = self.__filter_param(path, _get_key)
                    else:
                        use_type = escape_type

                    if use_type == 'url':
                        new_data[_get_key] = url_escape(_get_value)
                    elif use_type == 'script':
                        new_data[_get_key] = check_script(_get_value, 1)
                    elif use_type == 'name':
                        new_data[_get_key] = html_escape_name(_get_value)
                    else:
                        new_data[_get_key] = html_escape(_get_value, 1)
                except Exception as e:
                    logger.error(u"CheckXssMiddleware GET/POST参数 转换失败！%s" % e)
                    new_data[_get_key] = _get_value
            else:
                try:
                    new_data[_get_key] = html_escape(_get_value, 1, True)
                except Exception as e:
                    logger.error(u"CheckXssMiddleware GET/POST参数 转换失败！%s" % e)
                    new_data[_get_key] = _get_value
        # update 数据
        data_copy.update(new_data)
        return data_copy

    def __filter_param(self, path, param):
        """
        特殊path处理
        @param path: 路径
        @param param: 参数 
        @return: 'html/name/url/script'
        """
        use_name, use_url, use_script = self.__filter_path_list()
        try:
            result = 'html'
            # name过滤
            for name_path, name_v in use_name.items():
                is_path = re.match(r'^%s' % name_path, path)
                if is_path and param in name_v:
                    result = 'name'
                    break
            # url过滤
            if result == 'html':
                for url_path, url_v in use_url.items():
                    is_path = re.match(r'^%s' % url_path, path)
                    if is_path and param in url_v:
                        result = 'url'
                        break
            # script过滤
            if result == 'html':
                for script_path, script_v in use_script.items():
                    is_path = re.match(r'^%s' % script_path, path)
                    if is_path and param in script_v:
                        result = 'script'
                        break
        except Exception as e:
            logger.error(u"CheckXssMiddleware 特殊path处理失败！%s" % e)
            result = 'html'
        return result

    def __filter_path_list(self):
        """
        特殊path注册
        """
        use_name = {}
        use_url = {}
        use_script = {}
        return (use_name, use_url, use_script)


'''
管理员可查看错误详情
'''
class UserBasedExceptionMiddleware:
    def process_exception(self, request, exception):
        if request.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())
