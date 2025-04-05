#!/bin/bash

# 创建测试目录
mkdir -p test_images
mkdir -p watermarked_images

# 提示用户
echo "这是一个测试脚本，用于演示批量添加水印功能"
echo "请先准备：1.一个包含多张图片的文件夹  2.一张作为水印的图片"
echo ""
echo "示例用法："
echo "python watermark.py --input_dir ./test_images --output_dir ./watermarked_images --watermark ./logo.png --position bottom-right --margin 20 --scale 0.2"
echo ""

# 安装依赖
pip install -r requirements.txt 