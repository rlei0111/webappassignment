"""
数据库初始化脚本
创建所有数据表
"""
from app import app
from models import db

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表（谨慎使用）
        print("正在删除旧表...")
        db.drop_all()

        # 创建所有表
        print("正在创建新表...")
        db.create_all()

        print("数据库初始化完成！")
        print("已创建以下表：")
        print("- users (用户表)")
        print("- surveys (问卷表)")
        print("- questions (问题表)")
        print("- options (选项表)")
        print("- responses (回答记录表)")
        print("- answers (答案表)")

if __name__ == '__main__':
    init_database()
