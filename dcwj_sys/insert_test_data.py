"""
插入模拟测试数据
创建示例问卷、用户、提交记录
"""
from app import app
from models import db, User, Survey, Question, Option, Response, Answer
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def insert_test_data():
    """插入测试数据"""
    with app.app_context():
        print("开始插入测试数据...")

        # 1. 创建测试用户
        print("\n[1/5] 创建测试用户...")
        users = []

        # 普通用户
        for i in range(1, 6):
            user = User(
                username=f'user{i}',
                password=generate_password_hash('123456'),
                email=f'user{i}@example.com',
                role='user'
            )
            users.append(user)
            db.session.add(user)

        db.session.commit()
        print(f"创建了 {len(users)} 个测试用户")

        # 获取管理员
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("错误: 管理员账户不存在，请先运行 create_admin.py")
            return

        # 2. 创建测试问卷
        print("\n[2/5] 创建测试问卷...")

        # 问卷1: 客户满意度调查
        survey1 = Survey(
            title_zh='客户满意度调查',
            title_en='Customer Satisfaction Survey',
            description_zh='感谢您参与我们的客户满意度调查，您的反馈对我们非常重要！',
            description_en='Thank you for participating in our customer satisfaction survey. Your feedback is very important to us!',
            status='published',
            created_by=admin.id,
            start_time=datetime.utcnow() - timedelta(days=7),
            end_time=datetime.utcnow() + timedelta(days=30),
            allow_anonymous=True
        )
        db.session.add(survey1)
        db.session.flush()

        # 问卷1 - 问题1: 单选题
        q1 = Question(
            survey_id=survey1.id,
            question_text_zh='您对我们的服务总体满意度如何？',
            question_text_en='How satisfied are you with our service overall?',
            question_type='single',
            is_required=True,
            order_num=0
        )
        db.session.add(q1)
        db.session.flush()

        options_q1 = [
            ('非常满意', 'Very Satisfied'),
            ('满意', 'Satisfied'),
            ('一般', 'Neutral'),
            ('不满意', 'Dissatisfied'),
            ('非常不满意', 'Very Dissatisfied')
        ]
        for idx, (text_zh, text_en) in enumerate(options_q1):
            opt = Option(
                question_id=q1.id,
                option_text_zh=text_zh,
                option_text_en=text_en,
                order_num=idx
            )
            db.session.add(opt)

        # 问卷1 - 问题2: 多选题
        q2 = Question(
            survey_id=survey1.id,
            question_text_zh='您最看重我们的哪些方面？（可多选）',
            question_text_en='What aspects do you value most about us? (Multiple choices)',
            question_type='multiple',
            is_required=True,
            order_num=1
        )
        db.session.add(q2)
        db.session.flush()

        options_q2 = [
            ('产品质量', 'Product Quality'),
            ('服务态度', 'Service Attitude'),
            ('价格优惠', 'Competitive Price'),
            ('配送速度', 'Delivery Speed'),
            ('售后服务', 'After-sales Service')
        ]
        for idx, (text_zh, text_en) in enumerate(options_q2):
            opt = Option(
                question_id=q2.id,
                option_text_zh=text_zh,
                option_text_en=text_en,
                order_num=idx
            )
            db.session.add(opt)

        # 问卷1 - 问题3: 评分题
        q3 = Question(
            survey_id=survey1.id,
            question_text_zh='您会向朋友推荐我们的服务吗？（1-10分）',
            question_text_en='Would you recommend our service to friends? (1-10)',
            question_type='rating',
            is_required=True,
            order_num=2,
            rating_scale=10
        )
        db.session.add(q3)

        # 问卷1 - 问题4: 填空题
        q4 = Question(
            survey_id=survey1.id,
            question_text_zh='您对我们有什么建议或意见？',
            question_text_en='Do you have any suggestions or comments for us?',
            question_type='text',
            is_required=False,
            order_num=3,
            max_length=500
        )
        db.session.add(q4)

        db.session.commit()
        print(f"创建问卷: {survey1.title_zh} (4个问题)")

        # 问卷2: 产品反馈调查
        survey2 = Survey(
            title_zh='新产品反馈调查',
            title_en='New Product Feedback Survey',
            description_zh='我们推出了新产品，期待您的宝贵意见！',
            description_en='We have launched a new product and look forward to your valuable feedback!',
            status='published',
            created_by=admin.id,
            allow_anonymous=True
        )
        db.session.add(survey2)
        db.session.flush()

        # 问卷2 - 问题1: 单选题
        q5 = Question(
            survey_id=survey2.id,
            question_text_zh='您的年龄段是？',
            question_text_en='What is your age group?',
            question_type='single',
            is_required=True,
            order_num=0
        )
        db.session.add(q5)
        db.session.flush()

        options_q5 = [
            ('18岁以下', 'Under 18'),
            ('18-25岁', '18-25'),
            ('26-35岁', '26-35'),
            ('36-45岁', '36-45'),
            ('46岁以上', 'Over 46')
        ]
        for idx, (text_zh, text_en) in enumerate(options_q5):
            opt = Option(
                question_id=q5.id,
                option_text_zh=text_zh,
                option_text_en=text_en,
                order_num=idx
            )
            db.session.add(opt)

        # 问卷2 - 问题2: 评分题
        q6 = Question(
            survey_id=survey2.id,
            question_text_zh='您对新产品的外观设计评分（1-5分）',
            question_text_en='Rate the design of the new product (1-5)',
            question_type='rating',
            is_required=True,
            order_num=1,
            rating_scale=5
        )
        db.session.add(q6)

        db.session.commit()
        print(f"创建问卷: {survey2.title_zh} (2个问题)")

        # 问卷3: 草稿状态
        survey3 = Survey(
            title_zh='员工培训需求调查',
            title_en='Employee Training Needs Survey',
            description_zh='了解员工培训需求，提升团队能力',
            description_en='Understand employee training needs and improve team capabilities',
            status='draft',
            created_by=admin.id,
            allow_anonymous=False
        )
        db.session.add(survey3)
        db.session.flush()

        q7 = Question(
            survey_id=survey3.id,
            question_text_zh='您希望参加哪些培训？',
            question_text_en='What training would you like to attend?',
            question_type='multiple',
            is_required=True,
            order_num=0
        )
        db.session.add(q7)
        db.session.flush()

        options_q7 = [
            ('技术培训', 'Technical Training'),
            ('管理培训', 'Management Training'),
            ('沟通技巧', 'Communication Skills')
        ]
        for idx, (text_zh, text_en) in enumerate(options_q7):
            opt = Option(
                question_id=q7.id,
                option_text_zh=text_zh,
                option_text_en=text_en,
                order_num=idx
            )
            db.session.add(opt)

        db.session.commit()
        print(f"创建问卷: {survey3.title_zh} (草稿)")

        # 3. 创建模拟提交记录
        print("\n[3/5] 创建模拟提交记录...")

        # 为问卷1创建30条提交记录
        q1_options = Option.query.filter_by(question_id=q1.id).all()
        q2_options = Option.query.filter_by(question_id=q2.id).all()

        responses_count = 0
        used_user_ids = set()  # 记录已使用的用户ID，避免重复
        for i in range(30):
            # 随机选择用户或匿名
            if i < 10:
                # 确保每个用户只提交一次
                user_id = users[i % len(users)].id
                if user_id in used_user_ids:
                    user_id = None  # 如果用户已提交，改为匿名
                else:
                    used_user_ids.add(user_id)
                ip = f'192.168.1.{i+1}'
            else:
                user_id = None
                ip = f'10.0.0.{i+1}'

            response = Response(
                survey_id=survey1.id,
                user_id=user_id,
                ip_address=ip,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                submitted_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.session.add(response)
            db.session.flush()

            # 问题1答案 (单选)
            selected_option = random.choice(q1_options)
            answer1 = Answer(
                response_id=response.id,
                question_id=q1.id,
                option_id=selected_option.id
            )
            db.session.add(answer1)

            # 问题2答案 (多选)
            num_selections = random.randint(1, 3)
            selected_options = random.sample(q2_options, num_selections)
            for opt in selected_options:
                answer2 = Answer(
                    response_id=response.id,
                    question_id=q2.id,
                    option_id=opt.id
                )
                db.session.add(answer2)

            # 问题3答案 (评分)
            rating = random.randint(6, 10)
            answer3 = Answer(
                response_id=response.id,
                question_id=q3.id,
                rating_value=rating
            )
            db.session.add(answer3)

            # 问题4答案 (填空，50%概率填写)
            if random.random() > 0.5:
                comments = [
                    '服务很好，继续保持！',
                    '希望能提供更多优惠活动',
                    '配送速度可以再快一些',
                    '产品质量不错，很满意',
                    '客服态度很好，解决问题及时',
                    '价格有点贵，希望能降价',
                    '整体体验不错，会继续支持',
                    '建议增加更多产品种类'
                ]
                answer4 = Answer(
                    response_id=response.id,
                    question_id=q4.id,
                    answer_text=random.choice(comments)
                )
                db.session.add(answer4)

            responses_count += 1

        # 更新问卷1的提交次数
        survey1.response_count = responses_count

        # 为问卷2创建15条提交记录
        q5_options = Option.query.filter_by(question_id=q5.id).all()

        responses_count2 = 0
        used_user_ids2 = set()  # 记录已使用的用户ID，避免重复
        for i in range(15):
            if i % 2 == 0:
                user_id = None
            else:
                user_id = users[i % len(users)].id
                if user_id in used_user_ids2:
                    user_id = None  # 如果用户已提交，改为匿名
                else:
                    used_user_ids2.add(user_id)
            ip = f'172.16.0.{i+1}'

            response = Response(
                survey_id=survey2.id,
                user_id=user_id,
                ip_address=ip,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                submitted_at=datetime.utcnow() - timedelta(days=random.randint(0, 5))
            )
            db.session.add(response)
            db.session.flush()

            # 问题5答案 (单选)
            selected_option = random.choice(q5_options)
            answer5 = Answer(
                response_id=response.id,
                question_id=q5.id,
                option_id=selected_option.id
            )
            db.session.add(answer5)

            # 问题6答案 (评分)
            rating = random.randint(3, 5)
            answer6 = Answer(
                response_id=response.id,
                question_id=q6.id,
                rating_value=rating
            )
            db.session.add(answer6)

            responses_count2 += 1

        # 更新问卷2的提交次数
        survey2.response_count = responses_count2

        db.session.commit()
        print(f"为问卷1创建了 {responses_count} 条提交记录")
        print(f"为问卷2创建了 {responses_count2} 条提交记录")

        # 4. 统计信息
        print("\n[4/5] 数据统计...")
        total_users = User.query.count()
        total_surveys = Survey.query.count()
        total_questions = Question.query.count()
        total_responses = Response.query.count()
        total_answers = Answer.query.count()

        print(f"用户总数: {total_users}")
        print(f"问卷总数: {total_surveys}")
        print(f"问题总数: {total_questions}")
        print(f"提交记录: {total_responses}")
        print(f"答案总数: {total_answers}")

        print("\n[5/5] 测试数据插入完成！")
        print("\n" + "=" * 60)
        print("测试账户信息:")
        print("=" * 60)
        print("管理员账户:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n普通用户账户:")
        for i in range(1, 6):
            print(f"  用户名: user{i}")
            print(f"  密码: 123456")
        print("=" * 60)

if __name__ == '__main__':
    insert_test_data()
