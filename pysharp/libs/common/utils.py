# coding=utf-8
'''
公用方法

#===============================================================================
# 1.页面输入内容转义（防止xss攻击）
from common.utils import html_escape, url_escape
 
 # 转义html内容
 html_content = html_escape(input_content)
 
 # 转义url内容
 url_content = url_escape(input_content)
#===============================================================================
'''
from .pxfilter import XssHtml
from django.utils.http import urlencode
import httplib2
import json
from .log import logger
import traceback

def html_escape(str_escape, fromtype=0, is_json=False):
    """
    字符串转义为html代码
    @param str_escape: 需要解析的html代码
    @param fromtype: 来源，0：views函数，1：middleware
    @param is_json: 是否为json串 
    """
    try:
        result_str = escape_new(str_escape, fromtype, is_json)
        return result_str
    except Exception as e:
        return str_escape
    
    
def url_escape(url_escape):
    """
    转义url中的特殊字符
    @param str_escape: 需要解析的url
    """
    try:
        result_str = escape_url(url_escape)
        return result_str
    except Exception as e:
        return url_escape
    
    
def html_escape_name(str_escape):
    """
    字符串转义为html代码
    @param str_escape: 需要解析的html代码
    """
    try:
        result_str = escape_name(str_escape)
        return result_str
    except Exception as e:
        return str_escape
    
    
def escape_url(s):
    s = s.replace("<", "")
    s = s.replace(">", "")
    s = s.replace(' ', "")
    s = s.replace('"', "")
    s = s.replace("'", "")
    return s


def escape_name(s):
    '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated.
    rewrite the cgi method
    '''
    s = s.replace("&", "") # Must be done first!
    s = s.replace("<", "")
    s = s.replace(">", "")
    s = s.replace(' ', "")
    s = s.replace('"', "")
    s = s.replace("'", "")
    return s

def check_script(str_escape, fromtype=0):
    """
    防止js脚本注入
    @param str_escape: 要检测的字符串
    @param fromtype: 0：views，1：middleware
    """ 
    try:
        parser = XssHtml()
        parser.feed(str_escape)
        parser.close()
        return parser.getHtml()
    except Exception as e:
        return str_escape

def escape_new(s, fromtype, is_json):
    '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated.
    rewrite the cgi method
    @param fromtype: 来源，0：views函数，1：middleware（对&做转换），默认是0
    @param is_json: 是否为json串（True/False） ，默认为False
    '''
    # &转换
    if fromtype == 1 and not is_json:
        s = s.replace("&", "&amp;") # Must be done first!
    # <>转换
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    # 单双引号转换
    if not is_json:
        s = s.replace(' ', "&nbsp;")
        s = s.replace('"', "&quot;")
        s = s.replace("'", "&#39;")
    return s


def http_request_common(url, http_method, query=''):    
    '''
    @summary: 发起GET/POST等各种请求
    @param query: string,number,or a iterable obj
    @param http_method: GET / POST  等各种请求方式
    @note: httplib2的post里的数据值必须转成utf8编码
    @note: 优先选用django的querydict的urlencode, urllib的urlencode会出现编码问题。
    @note: 参照http://stackoverflow.com/questions/3110104/unicodeencodeerror-ascii-codec-cant-encode-character-when-trying-a-http-post
    @note: 请求参数query中的参数项如果是json, 请不要传入python dict, 一定要传入json字符串, 否则服务端将无法解析json(单双引号问题)
    @return: 直接返回原始响应数据(包含result,data,message的字典)
    '''
    # 如果是一个iterable，则转换成url的param字符串
    if hasattr(query, 'items'):
        query = urlencode(query)
    if http_method == 'POST':
        resp, content = httplib2.Http().request(url, http_method, body=query)
    else:
        uri = '%s?%s' % (url, query) if query else url
        resp, content = httplib2.Http().request(uri, 'GET')
    if resp.status==200:
        # 成功，返回content
        try:
            content_dict = json.loads(content)
            return content_dict
        except Exception as e:
            log_message = u"返回数据格式不正确，统一为json.\n uri：%s, content:%s.\n Exception: %s\n===>traceback format_exc: %s" % (
                                                                                                                           uri, content, e, traceback.format_exc())
            logger.error(log_message)
            return {'result':False, 'message':u"调用远程服务失败，Http请求返回数据格式错误!"}
    else:
        log_message = u"调用远程服务失败，Http请求错误状态码：%s\n%s\nurl:%s\nquery:%s" % (
                                                                  resp.status, http_method, url, query)
        logger.error(log_message)
        return {'result':False, 'message':u"调用远程服务失败，Http请求错误状态码：%s" % resp.status}



