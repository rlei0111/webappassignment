"""
管理员路由
处理问卷CRUD、预览、复制等管理功能
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import db, Survey, Question, Option
from utils.decorators import admin_required
from utils.i18n import _, get_locale

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理后台首页"""
    # 统计数据
    total_surveys = Survey.query.count()
    published_surveys = Survey.query.filter_by(status='published').count()
    draft_surveys = Survey.query.filter_by(status='draft').count()

    return render_template('admin/dashboard.html',
                         total_surveys=total_surveys,
                         published_surveys=published_surveys,
                         draft_surveys=draft_surveys,
                         locale=get_locale())


@admin_bp.route('/surveys')
@admin_required
def survey_list():
    """问卷列表"""
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)

    query = Survey.query

    # 状态筛选
    if status_filter in ['draft', 'published', 'closed']:
        query = query.filter_by(status=status_filter)

    # 按创建时间倒序
    surveys = query.order_by(Survey.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('admin/survey_list.html',
                         surveys=surveys,
                         status_filter=status_filter,
                         locale=get_locale())


@admin_bp.route('/surveys/create', methods=['GET', 'POST'])
@admin_required
def create_survey():
    """创建问卷"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            title_zh = request.form.get('title_zh', '').strip()
            title_en = request.form.get('title_en', '').strip()
            description_zh = request.form.get('description_zh', '').strip()
            description_en = request.form.get('description_en', '').strip()
            start_time_str = request.form.get('start_time', '').strip()
            end_time_str = request.form.get('end_time', '').strip()
            allow_anonymous = request.form.get('allow_anonymous') == 'on'

            # 验证必填项
            if not title_zh:
                flash(_('validation.required_field'), 'danger')
                return redirect(url_for('admin.create_survey'))

            # 处理时间
            start_time = None
            end_time = None
            if start_time_str:
                start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            if end_time_str:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

            # 创建问卷
            from flask import session
            survey = Survey(
                title_zh=title_zh,
                title_en=title_en if title_en else None,
                description_zh=description_zh if description_zh else None,
                description_en=description_en if description_en else None,
                status='draft',
                created_by=session['user_id'],
                start_time=start_time,
                end_time=end_time,
                allow_anonymous=allow_anonymous
            )
            db.session.add(survey)
            db.session.flush()

            # 处理问题
            question_count = int(request.form.get('question_count', 0))
            for i in range(question_count):
                question_text_zh = request.form.get(f'question_text_zh_{i}', '').strip()
                if not question_text_zh:
                    continue

                question_text_en = request.form.get(f'question_text_en_{i}', '').strip()
                question_type = request.form.get(f'question_type_{i}', 'single')
                is_required = request.form.get(f'is_required_{i}') == 'on'
                max_length = request.form.get(f'max_length_{i}', type=int)
                rating_scale = request.form.get(f'rating_scale_{i}', 5, type=int)

                question = Question(
                    survey_id=survey.id,
                    question_text_zh=question_text_zh,
                    question_text_en=question_text_en if question_text_en else None,
                    question_type=question_type,
                    is_required=is_required,
                    order_num=i,
                    max_length=max_length,
                    rating_scale=rating_scale
                )
                db.session.add(question)
                db.session.flush()

                # 处理选项（单选题和多选题）
                if question_type in ['single', 'multiple']:
                    option_count = int(request.form.get(f'option_count_{i}', 0))
                    for j in range(option_count):
                        option_text_zh = request.form.get(f'option_text_zh_{i}_{j}', '').strip()
                        if not option_text_zh:
                            continue

                        option_text_en = request.form.get(f'option_text_en_{i}_{j}', '').strip()
                        option = Option(
                            question_id=question.id,
                            option_text_zh=option_text_zh,
                            option_text_en=option_text_en if option_text_en else None,
                            order_num=j
                        )
                        db.session.add(option)

            db.session.commit()
            flash(_('message.create_success'), 'success')
            return redirect(url_for('admin.survey_list'))

        except Exception as e:
            db.session.rollback()
            flash(_('message.operation_failed'), 'danger')
            return redirect(url_for('admin.create_survey'))

    return render_template('admin/survey_create.html', locale=get_locale())


@admin_bp.route('/surveys/<int:survey_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_survey(survey_id):
    """编辑问卷（仅草稿状态）"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash(_('survey.survey_not_found'), 'danger')
        return redirect(url_for('admin.survey_list'))

    # 只能编辑草稿状态的问卷
    if survey.status != 'draft':
        flash(_('message.no_permission'), 'danger')
        return redirect(url_for('admin.survey_list'))

    if request.method == 'POST':
        try:
            # 更新基本信息
            survey.title_zh = request.form.get('title_zh', '').strip()
            survey.title_en = request.form.get('title_en', '').strip()
            survey.description_zh = request.form.get('description_zh', '').strip()
            survey.description_en = request.form.get('description_en', '').strip()

            start_time_str = request.form.get('start_time', '').strip()
            end_time_str = request.form.get('end_time', '').strip()
            survey.allow_anonymous = request.form.get('allow_anonymous') == 'on'

            if start_time_str:
                survey.start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            else:
                survey.start_time = None

            if end_time_str:
                survey.end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
            else:
                survey.end_time = None

            # 删除旧问题
            Question.query.filter_by(survey_id=survey.id).delete()

            # 添加新问题
            question_count = int(request.form.get('question_count', 0))
            for i in range(question_count):
                question_text_zh = request.form.get(f'question_text_zh_{i}', '').strip()
                if not question_text_zh:
                    continue

                question_text_en = request.form.get(f'question_text_en_{i}', '').strip()
                question_type = request.form.get(f'question_type_{i}', 'single')
                is_required = request.form.get(f'is_required_{i}') == 'on'
                max_length = request.form.get(f'max_length_{i}', type=int)
                rating_scale = request.form.get(f'rating_scale_{i}', 5, type=int)

                question = Question(
                    survey_id=survey.id,
                    question_text_zh=question_text_zh,
                    question_text_en=question_text_en if question_text_en else None,
                    question_type=question_type,
                    is_required=is_required,
                    order_num=i,
                    max_length=max_length,
                    rating_scale=rating_scale
                )
                db.session.add(question)
                db.session.flush()

                # 处理选项
                if question_type in ['single', 'multiple']:
                    option_count = int(request.form.get(f'option_count_{i}', 0))
                    for j in range(option_count):
                        option_text_zh = request.form.get(f'option_text_zh_{i}_{j}', '').strip()
                        if not option_text_zh:
                            continue

                        option_text_en = request.form.get(f'option_text_en_{i}_{j}', '').strip()
                        option = Option(
                            question_id=question.id,
                            option_text_zh=option_text_zh,
                            option_text_en=option_text_en if option_text_en else None,
                            order_num=j
                        )
                        db.session.add(option)

            db.session.commit()
            flash(_('message.update_success'), 'success')
            return redirect(url_for('admin.survey_list'))

        except Exception as e:
            db.session.rollback()
            flash(_('message.operation_failed'), 'danger')

    return render_template('admin/survey_edit.html', survey=survey, locale=get_locale())


@admin_bp.route('/surveys/<int:survey_id>/delete', methods=['POST'])
@admin_required
def delete_survey(survey_id):
    """删除问卷"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        return jsonify({'success': False, 'message': _('survey.survey_not_found')})

    try:
        db.session.delete(survey)
        db.session.commit()
        return jsonify({'success': True, 'message': _('message.delete_success')})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': _('message.operation_failed')})


@admin_bp.route('/surveys/<int:survey_id>/publish', methods=['POST'])
@admin_required
def publish_survey(survey_id):
    """发布问卷"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        return jsonify({'success': False, 'message': _('survey.survey_not_found')})

    try:
        survey.status = 'published'
        db.session.commit()
        return jsonify({'success': True, 'message': _('message.publish_success')})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': _('message.operation_failed')})


@admin_bp.route('/surveys/<int:survey_id>/close', methods=['POST'])
@admin_required
def close_survey(survey_id):
    """关闭问卷"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        return jsonify({'success': False, 'message': _('survey.survey_not_found')})

    try:
        survey.status = 'closed'
        db.session.commit()
        return jsonify({'success': True, 'message': _('message.close_success')})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': _('message.operation_failed')})


@admin_bp.route('/surveys/<int:survey_id>/copy', methods=['POST'])
@admin_required
def copy_survey(survey_id):
    """复制问卷"""
    original_survey = db.session.get(Survey, survey_id)
    if not original_survey:
        return jsonify({'success': False, 'message': _('survey.survey_not_found')})

    try:
        from flask import session

        # 创建新问卷
        new_survey = Survey(
            title_zh=original_survey.title_zh + ' (副本)',
            title_en=original_survey.title_en + ' (Copy)' if original_survey.title_en else None,
            description_zh=original_survey.description_zh,
            description_en=original_survey.description_en,
            status='draft',
            created_by=session['user_id'],
            start_time=original_survey.start_time,
            end_time=original_survey.end_time,
            allow_anonymous=original_survey.allow_anonymous
        )
        db.session.add(new_survey)
        db.session.flush()

        # 复制问题
        for question in original_survey.questions:
            new_question = Question(
                survey_id=new_survey.id,
                question_text_zh=question.question_text_zh,
                question_text_en=question.question_text_en,
                question_type=question.question_type,
                is_required=question.is_required,
                order_num=question.order_num,
                max_length=question.max_length,
                rating_scale=question.rating_scale
            )
            db.session.add(new_question)
            db.session.flush()

            # 复制选项
            for option in question.options:
                new_option = Option(
                    question_id=new_question.id,
                    option_text_zh=option.option_text_zh,
                    option_text_en=option.option_text_en,
                    order_num=option.order_num
                )
                db.session.add(new_option)

        db.session.commit()
        return jsonify({'success': True, 'message': _('message.copy_success')})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': _('message.operation_failed')})


@admin_bp.route('/surveys/<int:survey_id>/preview')
@admin_required
def preview_survey(survey_id):
    """预览问卷"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash(_('survey.survey_not_found'), 'danger')
        return redirect(url_for('admin.survey_list'))

    questions = Question.query.filter_by(survey_id=survey_id).order_by(Question.order_num).all()

    return render_template('admin/survey_preview.html',
                         survey=survey,
                         questions=questions,
                         locale=get_locale(),
                         preview_mode=True)
