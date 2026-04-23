@echo off
echo ========================================
echo 问卷调查系统 - 环境配置脚本
echo ========================================
echo.

echo [1/4] 创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo 错误: 虚拟环境创建失败
    pause
    exit /b 1
)
echo 虚拟环境创建成功！
echo.

echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat
echo.

echo [3/4] 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)
echo 依赖包安装成功！
echo.

echo [4/4] 初始化数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo 错误: 数据库初始化失败
    pause
    exit /b 1
)
echo.

echo 创建管理员账户...
python create_admin.py
echo.

echo ========================================
echo 环境配置完成！
echo ========================================
echo.
echo 启动应用: python app.py
echo 访问地址: http://localhost:5000
echo.
pause
