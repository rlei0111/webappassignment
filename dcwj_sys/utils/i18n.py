"""
国际化工具函数
提供多语言支持
"""
import json
import os
from flask import request

# 翻译缓存
_translations_cache = {}


def load_translations(locale):
    """
    加载翻译文件

    Args:
        locale (str): 语言代码，如 'zh_CN' 或 'en_US'

    Returns:
        dict: 翻译字典
    """
    if locale in _translations_cache:
        return _translations_cache[locale]

    try:
        file_path = os.path.join('translations', f'{locale}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translations_cache[locale] = translations
            return translations
    except FileNotFoundError:
        # 默认返回中文
        if locale != 'zh_CN':
            return load_translations('zh_CN')
        return {}


def get_locale():
    """
    获取当前语言

    Returns:
        str: 语言代码
    """
    # 优先从Cookie获取
    locale = request.cookies.get('locale')
    if locale in ['en_US']:
        return locale

    # 默认使用英文
    return 'en_US'


def get_translation(key, locale=None):
    """
    获取翻译文本

    Args:
        key (str): 翻译键，支持嵌套如 'auth.login_title'
        locale (str): 语言代码，默认使用当前语言

    Returns:
        str: 翻译后的文本
    """
    if locale is None:
        locale = get_locale()

    translations = load_translations(locale)

    # 支持嵌套键
    keys = key.split('.')
    value = translations
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return key

    return value if isinstance(value, str) else key


def _(key):
    """
    翻译函数简写

    Args:
        key (str): 翻译键

    Returns:
        str: 翻译后的文本
    """
    return get_translation(key)


def init_translations():
    """初始化翻译缓存（应用启动时调用）"""
    load_translations('en_US')
