"""
Flask 应用入口
初始化应用、注册蓝图、配置数据库
"""
from flask import Flask, render_template
from config import config
from models import db
from utils.i18n import get_locale, get_translation

# 创建应用实例
app = Flask(__name__)

# 加载配置
app.config.from_object(config['development'])

# 初始化数据库
db.init_app(app)

# 注册蓝图
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.survey import survey_bp
from routes.stats import stats_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(survey_bp)
app.register_blueprint(stats_bp)


# 注册模板全局函数
@app.context_processor
def inject_functions():
    """注入模板全局函数"""
    return {
        '_': get_translation,
        'get_locale': get_locale
    }


# 首页路由
@app.route('/')
def index():
    """首页 - 显示所有已发布的问卷"""
    from models import Survey
    from utils.i18n import get_locale
    from datetime import datetime

    # 获取所有已发布的问卷
    surveys = Survey.query.filter_by(status='published').order_by(Survey.created_at.desc()).all()

    # 过滤有效期内的问卷
    valid_surveys = []
    for survey in surveys:
        if survey.is_available():
            valid_surveys.append(survey)

    return render_template('index.html', surveys=valid_surveys, locale=get_locale())


# 错误处理
@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
