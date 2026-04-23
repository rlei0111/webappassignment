"""
权限装饰器
提供登录验证和管理员权限验证
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from utils.i18n import _


def login_required(f):
    """
    登录验证装饰器
    要求用户必须登录才能访问

    Args:
        f: 被装饰的函数

    Returns:
        装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('message.no_permission'), 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    管理员权限验证装饰器
    要求用户必须是管理员才能访问

    Args:
        f: 被装饰的函数

    Returns:
        装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('message.no_permission'), 'warning')
            return redirect(url_for('auth.login'))

        # 检查用户角色
        from models import User, db
        user = db.session.get(User, session.get('user_id'))
        if not user or user.role != 'admin':
            flash(_('message.no_permission'), 'danger')
            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """
    获取当前登录用户

    Returns:
        User: 当前用户对象，未登录返回None
    """
    if 'user_id' not in session:
        return None

    from models import User, db
    return db.session.get(User, session.get('user_id'))
