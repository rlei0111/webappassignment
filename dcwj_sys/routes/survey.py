"""
问卷填写路由
处理问卷填写、提交、查看记录功能
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Survey, Question, Response, Answer
from utils.i18n import _, get_locale
from utils.helpers import get_client_ip, get_user_agent

survey_bp = Blueprint('survey', __name__, url_prefix='/survey')


@survey_bp.route('/<int:survey_id>')
def view(survey_id):
    """查看问卷（填写页面）"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash(_('survey.survey_not_found'), 'danger')
        return redirect(url_for('index'))

    # 检查问卷状态
    if survey.status != 'published':
        flash(_('survey.survey_closed'), 'warning')
        return redirect(url_for('index'))

    # 检查有效期
    if not survey.is_available():
        if survey.start_time and survey.start_time > db.func.now():
            flash(_('survey.survey_not_started'), 'warning')
        else:
            flash(_('survey.survey_expired'), 'warning')
        return redirect(url_for('index'))

    # 检查是否已提交
    user_id = session.get('user_id')
    ip_address = get_client_ip()

    if user_id:
        # 已登录用户检查
        existing = Response.query.filter_by(survey_id=survey_id, user_id=user_id).first()
        if existing:
            flash(_('survey.already_submitted'), 'warning')
            return redirect(url_for('index'))
    else:
        # 游客检查
        existing = Response.query.filter_by(survey_id=survey_id, ip_address=ip_address).first()
        if existing:
            flash(_('survey.already_submitted'), 'warning')
            return redirect(url_for('index'))

    # 获取问题列表
    questions = Question.query.filter_by(survey_id=survey_id).order_by(Question.order_num).all()

    return render_template('survey/view.html',
                         survey=survey,
                         questions=questions,
                         locale=get_locale())


@survey_bp.route('/<int:survey_id>/submit', methods=['POST'])
def submit(survey_id):
    """提交问卷"""
    survey = db.session.get(Survey, survey_id)
    if not survey or survey.status != 'published':
        flash(_('survey.survey_closed'), 'danger')
        return redirect(url_for('index'))

    # 检查有效期
    if not survey.is_available():
        flash(_('survey.survey_expired'), 'warning')
        return redirect(url_for('index'))

    user_id = session.get('user_id')
    ip_address = get_client_ip()
    user_agent = get_user_agent()

    # 再次检查是否已提交
    if user_id:
        existing = Response.query.filter_by(survey_id=survey_id, user_id=user_id).first()
        if existing:
            flash(_('survey.already_submitted'), 'warning')
            return redirect(url_for('index'))
    else:
        existing = Response.query.filter_by(survey_id=survey_id, ip_address=ip_address).first()
        if existing:
            flash(_('survey.already_submitted'), 'warning')
            return redirect(url_for('index'))

    try:
        # 创建回答记录
        response = Response(
            survey_id=survey_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(response)
        db.session.flush()

        # 获取所有问题
        questions = Question.query.filter_by(survey_id=survey_id).all()

        # 处理答案
        for question in questions:
            # 验证必填项
            if question.is_required:
                if question.question_type in ['single', 'multiple']:
                    answer_key = f'question_{question.id}'
                    if answer_key not in request.form:
                        raise ValueError(f'Question {question.id} is required')
                elif question.question_type == 'text':
                    answer_text = request.form.get(f'question_{question.id}', '').strip()
                    if not answer_text:
                        raise ValueError(f'Question {question.id} is required')
                elif question.question_type == 'rating':
                    rating_value = request.form.get(f'question_{question.id}', type=int)
                    if not rating_value:
                        raise ValueError(f'Question {question.id} is required')

            # 保存答案
            if question.question_type == 'single':
                # 单选题
                option_id = request.form.get(f'question_{question.id}', type=int)
                if option_id:
                    answer = Answer(
                        response_id=response.id,
                        question_id=question.id,
                        option_id=option_id
                    )
                    db.session.add(answer)

            elif question.question_type == 'multiple':
                # 多选题：一个选项一条记录
                option_ids = request.form.getlist(f'question_{question.id}')
                for option_id in option_ids:
                    if option_id:
                        answer = Answer(
                            response_id=response.id,
                            question_id=question.id,
                            option_id=int(option_id)
                        )
                        db.session.add(answer)

            elif question.question_type == 'text':
                # 填空题
                answer_text = request.form.get(f'question_{question.id}', '').strip()
                if answer_text:
                    # 检查最大长度
                    if question.max_length and len(answer_text) > question.max_length:
                        raise ValueError(f'Text too long for question {question.id}')

                    answer = Answer(
                        response_id=response.id,
                        question_id=question.id,
                        answer_text=answer_text
                    )
                    db.session.add(answer)

            elif question.question_type == 'rating':
                # 评分题
                rating_value = request.form.get(f'question_{question.id}', type=int)
                if rating_value:
                    # 验证评分范围
                    if rating_value < 1 or rating_value > question.rating_scale:
                        raise ValueError(f'Invalid rating for question {question.id}')

                    answer = Answer(
                        response_id=response.id,
                        question_id=question.id,
                        rating_value=rating_value
                    )
                    db.session.add(answer)

        # 更新问卷提交次数
        survey.response_count += 1

        db.session.commit()
        flash(_('survey.submit_success'), 'success')
        return redirect(url_for('survey.success'))

    except ValueError as e:
        db.session.rollback()
        flash(_('validation.required_field'), 'danger')
        return redirect(url_for('survey.view', survey_id=survey_id))
    except Exception as e:
        db.session.rollback()
        flash(_('message.operation_failed'), 'danger')
        return redirect(url_for('survey.view', survey_id=survey_id))


@survey_bp.route('/success')
def success():
    """提交成功页面"""
    return render_template('survey/success.html', locale=get_locale())


@survey_bp.route('/my-responses')
def my_responses():
    """我的提交记录（需要登录）"""
    user_id = session.get('user_id')
    if not user_id:
        flash(_('message.no_permission'), 'warning')
        return redirect(url_for('auth.login'))

    # 获取用户的提交记录
    responses = Response.query.filter_by(user_id=user_id).order_by(Response.submitted_at.desc()).all()

    return render_template('survey/my_responses.html',
                         responses=responses,
                         locale=get_locale())
