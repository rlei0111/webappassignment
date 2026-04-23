"""
数据库模型定义
包含所有数据表的ORM模型
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.Enum('user', 'admin'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    surveys = db.relationship('Survey', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Survey(db.Model):
    """问卷表"""
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title_zh = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    description_zh = db.Column(db.Text)
    description_en = db.Column(db.Text)
    status = db.Column(db.Enum('draft', 'published', 'closed'), default='draft', nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    response_count = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    allow_anonymous = db.Column(db.Boolean, default=True)

    # 关系
    questions = db.relationship('Question', backref='survey', lazy='dynamic',
                               cascade='all, delete-orphan', order_by='Question.order_num')
    responses = db.relationship('Response', backref='survey', lazy='dynamic', cascade='all, delete-orphan')

    def get_title(self, locale='zh_CN'):
        """根据语言获取标题"""
        if locale == 'en_US' and self.title_en:
            return self.title_en
        return self.title_zh

    def get_description(self, locale='zh_CN'):
        """根据语言获取描述"""
        if locale == 'en_US' and self.description_en:
            return self.description_en
        return self.description_zh or ''

    def is_available(self):
        """检查问卷是否在有效期内"""
        now = datetime.utcnow()
        if self.start_time and now < self.start_time:
            return False
        if self.end_time and now > self.end_time:
            return False
        return True

    def __repr__(self):
        return f'<Survey {self.title_zh}>'


class Question(db.Model):
    """问题表"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    question_text_zh = db.Column(db.Text, nullable=False)
    question_text_en = db.Column(db.Text)
    question_type = db.Column(db.Enum('single', 'multiple', 'text', 'rating'), nullable=False)
    is_required = db.Column(db.Boolean, default=False)
    order_num = db.Column(db.Integer, nullable=False)
    max_length = db.Column(db.Integer)
    rating_scale = db.Column(db.Integer, default=5)

    # 关系
    options = db.relationship('Option', backref='question', lazy='dynamic',
                            cascade='all, delete-orphan', order_by='Option.order_num')
    answers = db.relationship('Answer', backref='question', lazy='dynamic', cascade='all, delete-orphan')

    def get_text(self, locale='zh_CN'):
        """根据语言获取问题文本"""
        if locale == 'en_US' and self.question_text_en:
            return self.question_text_en
        return self.question_text_zh

    def __repr__(self):
        return f'<Question {self.id}>'


class Option(db.Model):
    """选项表"""
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text_zh = db.Column(db.String(200), nullable=False)
    option_text_en = db.Column(db.String(200))
    order_num = db.Column(db.Integer, nullable=False)

    # 关系
    answers = db.relationship('Answer', backref='option', lazy='dynamic')

    def get_text(self, locale='zh_CN'):
        """根据语言获取选项文本"""
        if locale == 'en_US' and self.option_text_en:
            return self.option_text_en
        return self.option_text_zh

    def __repr__(self):
        return f'<Option {self.id}>'


class Response(db.Model):
    """回答记录表"""
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(255))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    answers = db.relationship('Answer', backref='response', lazy='dynamic', cascade='all, delete-orphan')

    # 索引
    __table_args__ = (
        db.Index('idx_survey_ip', 'survey_id', 'ip_address'),
        db.UniqueConstraint('survey_id', 'user_id', name='unique_user_response'),
    )

    def __repr__(self):
        return f'<Response {self.id}>'


class Answer(db.Model):
    """答案表"""
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    answer_text = db.Column(db.Text)
    rating_value = db.Column(db.Integer)

    def __repr__(self):
        return f'<Answer {self.id}>'
