"""
创建数据库脚本
先创建数据库，再初始化表
"""
import pymysql

def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='admin123',
            port=3306,
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS dcwj CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库 'dcwj' 创建成功！")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False

    return True

if __name__ == '__main__':
    if create_database():
        print("\n现在可以运行 init_db.py 来创建数据表")
