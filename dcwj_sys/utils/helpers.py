"""
辅助函数
提供通用的工具函数
"""
from flask import request


def get_client_ip():
    """
    获取客户端IP地址

    Returns:
        str: IP地址
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


def get_user_agent():
    """
    获取用户浏览器信息

    Returns:
        str: User-Agent字符串
    """
    return request.headers.get('User-Agent', '')[:255]
