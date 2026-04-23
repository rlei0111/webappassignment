"""
认证路由
处理用户注册、登录、登出、语言切换
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils.i18n import _, get_locale

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()

        # 验证输入
        if not username:
            flash(_('auth.username_required'), 'danger')
            return redirect(url_for('auth.register'))

        if not password:
            flash(_('auth.password_required'), 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash(_('validation.password_too_short'), 'danger')
            return redirect(url_for('auth.register'))

        # 检查用户名是否存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(_('auth.username_exists'), 'danger')
            return redirect(url_for('auth.register'))

        # 创建新用户
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                password=hashed_password,
                email=email if email else None,
                role='user'
            )
            db.session.add(new_user)
            db.session.commit()

            flash(_('auth.register_success'), 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(_('message.operation_failed'), 'danger')
            return redirect(url_for('auth.register'))

    return render_template('register.html', locale=get_locale())


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # 验证输入
        if not username or not password:
            flash(_('auth.login_failed'), 'danger')
            return redirect(url_for('auth.login'))

        # 查询用户
        user = User.query.filter_by(username=username).first()

        # 验证密码
        if user and check_password_hash(user.password, password):
            # 登录成功，设置session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session.permanent = True

            flash(_('auth.login_success'), 'success')

            # 根据角色跳转
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash(_('auth.login_failed'), 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html', locale=get_locale())


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash(_('auth.logout_success'), 'success')
    return redirect(url_for('index'))


@auth_bp.route('/set-language')
def set_language():
    """切换语言"""
    lang = request.args.get('lang', 'en_US')

    # 验证语言代码
    if lang not in ['en_US']:
        lang = 'en_US'

    # 设置Cookie
    response = make_response(redirect(request.referrer or url_for('index')))
    response.set_cookie('locale', lang, max_age=31536000)  # 1年

    return response
