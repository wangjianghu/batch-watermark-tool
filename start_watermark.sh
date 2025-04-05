#!/bin/bash

echo "正在启动批量图片添加水印工具..."

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 检查Python是否存在
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未检测到Python，请确保已安装Python 3。"
        echo "按回车键退出..."
        read
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# 检查主程序是否存在
if [ ! -f "$SCRIPT_DIR/watermark_gui.py" ]; then
    echo "错误: 找不到水印工具主程序 (watermark_gui.py)"
    echo "请确保该文件与启动脚本在同一目录。"
    echo "按回车键退出..."
    read
    exit 1
fi

# 启动水印工具
$PYTHON_CMD "$SCRIPT_DIR/watermark_gui.py"

# 如果出错
if [ $? -ne 0 ]; then
    echo "启动过程中出现错误，错误代码: $?"
    echo "按回车键退出..."
    read
fi 