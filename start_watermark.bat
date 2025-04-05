@echo off
echo 正在启动批量图片添加水印工具...

:: 获取批处理文件所在的目录
set SCRIPT_DIR=%~dp0

:: 切换到脚本目录
cd /d "%SCRIPT_DIR%"

:: 检查Python是否存在
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未检测到Python，请确保已安装Python并添加到PATH环境变量中。
    pause
    exit /b 1
)

:: 检查主程序是否存在
if not exist "%SCRIPT_DIR%watermark_gui.py" (
    echo 错误: 找不到水印工具主程序 (watermark_gui.py)
    echo 请确保该文件与启动脚本在同一目录。
    pause
    exit /b 1
)

:: 启动水印工具
python "%SCRIPT_DIR%watermark_gui.py"

:: 如果出错，等待用户按键
if %ERRORLEVEL% NEQ 0 (
    echo 启动过程中出现错误，错误代码: %ERRORLEVEL%
    pause
) 