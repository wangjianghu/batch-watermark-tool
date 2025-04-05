#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
批量图片添加水印工具启动脚本
此脚本可以在任意路径下启动水印工具的图形界面
"""

import os
import sys
import subprocess

def main():
    # 获取当前脚本所在的绝对路径
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    
    # 构建水印工具主程序路径
    watermark_gui_path = os.path.join(script_dir, "watermark_gui.py")
    
    # 检查主程序是否存在
    if not os.path.exists(watermark_gui_path):
        print("错误: 找不到水印工具主程序 (watermark_gui.py)")
        print(f"请确保 {watermark_gui_path} 文件存在")
        input("按回车键退出...")
        return
    
    try:
        # 设置工作目录为脚本所在目录
        os.chdir(script_dir)
        
        # 启动水印工具图形界面
        print("正在启动水印工具...")
        
        # 使用当前Python解释器启动程序
        python_executable = sys.executable
        subprocess.run([python_executable, watermark_gui_path])
        
    except Exception as e:
        print(f"启动过程中出现错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 