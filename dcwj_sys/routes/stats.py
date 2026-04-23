"""
统计分析路由
处理统计分析、图表展示、数据导出功能
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from sqlalchemy import func
from models import db, Survey, Question, Option, Response, Answer
from utils.decorators import admin_required
from utils.i18n import _, get_locale
import csv
from io import StringIO

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')


@stats_bp.route('/survey/<int:survey_id>')
@admin_required
def overview(survey_id):
    """统计概览"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash(_('survey.survey_not_found'), 'danger')
        return redirect(url_for('admin.survey_list'))

    # 获取总提交数
    total_responses = Response.query.filter_by(survey_id=survey_id).count()

    # 获取问题列表
    questions = Question.query.filter_by(survey_id=survey_id).order_by(Question.order_num).all()

    # 统计每个问题的数据
    stats_data = []
    for question in questions:
        question_stats = {
            'question': question,
            'data': None
        }

        if question.question_type in ['single', 'multiple']:
            # 选择题统计
            option_stats = []
            options = Option.query.filter_by(question_id=question.id).order_by(Option.order_num).all()

            for option in options:
                # 统计该选项被选择的次数
                count = Answer.query.filter_by(
                    question_id=question.id,
                    option_id=option.id
                ).count()

                percentage = (count / total_responses * 100) if total_responses > 0 else 0

                option_stats.append({
                    'option': option,
                    'count': count,
                    'percentage': round(percentage, 2)
                })

            question_stats['data'] = option_stats

        elif question.question_type == 'text':
            # 填空题：获取所有答案
            answers = Answer.query.filter_by(question_id=question.id).all()
            question_stats['data'] = [a.answer_text for a in answers if a.answer_text]

        elif question.question_type == 'rating':
            # 评分题统计
            # 计算平均分
            avg_rating = db.session.query(func.avg(Answer.rating_value)).filter(
                Answer.question_id == question.id
            ).scalar()

            # 统计各分数的分布
            rating_distribution = {}
            for i in range(1, question.rating_scale + 1):
                count = Answer.query.filter_by(
                    question_id=question.id,
                    rating_value=i
                ).count()
                rating_distribution[i] = count

            question_stats['data'] = {
                'average': round(avg_rating, 2) if avg_rating else 0,
                'distribution': rating_distribution,
                'total': sum(rating_distribution.values())
            }

        stats_data.append(question_stats)

    return render_template('stats/overview.html',
                         survey=survey,
                         total_responses=total_responses,
                         stats_data=stats_data,
                         locale=get_locale())


@stats_bp.route('/survey/<int:survey_id>/export')
@admin_required
def export_data(survey_id):
    """导出统计数据为CSV"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash(_('survey.survey_not_found'), 'danger')
        return redirect(url_for('admin.survey_list'))

    # 创建CSV
    output = StringIO()
    writer = csv.writer(output)

    # 写入标题行
    headers = ['Response ID', 'User ID', 'IP Address', 'Submitted At']
    questions = Question.query.filter_by(survey_id=survey_id).order_by(Question.order_num).all()
    for q in questions:
        headers.append(f'Q{q.order_num + 1}: {q.question_text_zh}')
    writer.writerow(headers)

    # 写入数据行
    responses = Response.query.filter_by(survey_id=survey_id).order_by(Response.submitted_at).all()
    for response in responses:
        row = [
            response.id,
            response.user_id or 'Anonymous',
            response.ip_address,
            response.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        ]

        # 获取每个问题的答案
        for question in questions:
            answers = Answer.query.filter_by(
                response_id=response.id,
                question_id=question.id
            ).all()

            if question.question_type == 'single':
                # 单选题
                if answers and answers[0].option_id:
                    option = db.session.get(Option, answers[0].option_id)
                    row.append(option.option_text_zh if option else '')
                else:
                    row.append('')

            elif question.question_type == 'multiple':
                # 多选题：多个选项用分号分隔
                option_texts = []
                for answer in answers:
                    if answer.option_id:
                        option = db.session.get(Option, answer.option_id)
                        if option:
                            option_texts.append(option.option_text_zh)
                row.append('; '.join(option_texts))

            elif question.question_type == 'text':
                # 填空题
                if answers:
                    row.append(answers[0].answer_text or '')
                else:
                    row.append('')

            elif question.question_type == 'rating':
                # 评分题
                if answers:
                    row.append(str(answers[0].rating_value or ''))
                else:
                    row.append('')

        writer.writerow(row)

    # 生成响应
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=survey_{survey_id}_data.csv'

    return response


@stats_bp.route('/survey/<int:survey_id>/chart-data')
@admin_required
def chart_data(survey_id):
    """获取图表数据（JSON格式）"""
    from flask import jsonify

    survey = db.session.get(Survey, survey_id)
    if not survey:
        return jsonify({'error': 'Survey not found'}), 404

    question_id = request.args.get('question_id', type=int)
    if not question_id:
        return jsonify({'error': 'Question ID required'}), 400

    question = db.session.get(Question, question_id)
    if not question or question.survey_id != survey_id:
        return jsonify({'error': 'Question not found'}), 404

    total_responses = Response.query.filter_by(survey_id=survey_id).count()

    if question.question_type in ['single', 'multiple']:
        # 选择题图表数据
        options = Option.query.filter_by(question_id=question_id).order_by(Option.order_num).all()
        labels = []
        data = []

        for option in options:
            count = Answer.query.filter_by(
                question_id=question_id,
                option_id=option.id
            ).count()

            labels.append(option.get_text(get_locale()))
            data.append(count)

        return jsonify({
            'type': 'pie',
            'labels': labels,
            'data': data
        })

    elif question.question_type == 'rating':
        # 评分题图表数据
        labels = []
        data = []

        for i in range(1, question.rating_scale + 1):
            count = Answer.query.filter_by(
                question_id=question_id,
                rating_value=i
            ).count()

            labels.append(str(i))
            data.append(count)

        return jsonify({
            'type': 'bar',
            'labels': labels,
            'data': data
        })

    return jsonify({'error': 'Invalid question type'}), 400
