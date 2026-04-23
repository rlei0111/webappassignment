"""
创建管理员账户脚本
"""
from app import app
from models import db, User
from werkzeug.security import generate_password_hash

def create_admin():
    """创建管理员账户"""
    with app.app_context():
        # 检查管理员是否已存在
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("管理员账户已存在！")
            print(f"用户名: admin")
            return

        # 创建管理员
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            email='admin@example.com',
            role='admin'
        )

        db.session.add(admin)
        db.session.commit()

        print("管理员账户创建成功！")
        print("=" * 50)
        print("用户名: admin")
        print("密码: admin123")
        print("角色: 管理员")
        print("=" * 50)
        print("请登录后台管理系统")

if __name__ == '__main__':
    create_admin()
