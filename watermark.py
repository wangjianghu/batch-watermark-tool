#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rectangle(draw, rect, color, radius):
    """绘制圆角矩形

    参数:
        draw: ImageDraw对象
        rect: 矩形区域 (left, top, right, bottom)
        color: 填充颜色，RGBA格式
        radius: 圆角半径
    """
    # 限制半径大小，避免超出矩形尺寸
    x0, y0, x1, y1 = rect
    width, height = x1 - x0, y1 - y0
    radius = min(radius, min(width, height) // 2)
    
    # 如果半径为0，直接绘制矩形
    if radius <= 0:
        draw.rectangle(rect, fill=color)
        return
    
    # 绘制圆角矩形
    # 绘制中间矩形
    draw.rectangle((x0, y0 + radius, x1, y1 - radius), fill=color)
    draw.rectangle((x0 + radius, y0, x1 - radius, y1), fill=color)
    
    # 绘制四个圆角
    # 左上角
    draw.pieslice((x0, y0, x0 + radius * 2, y0 + radius * 2), 180, 270, fill=color)
    # 右上角
    draw.pieslice((x1 - radius * 2, y0, x1, y0 + radius * 2), 270, 0, fill=color)
    # 左下角
    draw.pieslice((x0, y1 - radius * 2, x0 + radius * 2, y1), 90, 180, fill=color)
    # 右下角
    draw.pieslice((x1 - radius * 2, y1 - radius * 2, x1, y1), 0, 90, fill=color)

def add_text_watermark(input_path, output_path, text, font_size=40, font_color=(255, 255, 255, 128), position='bottom-right', margins=20, scale=0.2, bg_color=(0, 0, 0, 0), corner_radius=0):
    """
    给图片添加文字水印
    
    参数：
        input_path: 输入图片路径
        output_path: 输出图片路径
        text: 水印文字内容
        font_size: 字体大小
        font_color: 字体颜色，RGBA格式
        position: 水印位置，可选值：'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        margins: 水印边距，可以是整数（所有边距相同）或字典（指定不同方向的边距）
        scale: 水印缩放比例，0-1之间的小数
        bg_color: 水印背景颜色，RGBA格式
        corner_radius: 背景矩形的圆角半径（像素）
    """
    try:
        # 打开原始图片
        image = Image.open(input_path).convert('RGBA')
        width, height = image.size
        
        # 创建透明图层用于绘制文字
        txt = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt)
        
        # 尝试获取默认字体
        try:
            # 尝试加载系统字体
            system_fonts = [
                # macOS 常见中文字体
                '/System/Library/Fonts/PingFang.ttc',
                '/Library/Fonts/Arial Unicode.ttf',
                # Windows 常见中文字体
                'C:\\Windows\\Fonts\\simhei.ttf',
                'C:\\Windows\\Fonts\\msyh.ttc',
                # Linux 常见中文字体
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
            ]
            
            font = None
            for font_path in system_fonts:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
                    
            if font is None:
                # 如果找不到系统字体，使用PIL默认字体
                font = ImageFont.load_default()
        except Exception:
            # 使用默认字体
            font = ImageFont.load_default()
        
        # 计算文字大小
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else font.getsize(text)
        
        # 根据缩放比例调整文字大小
        adjusted_font_size = int(font_size * scale * width / text_width) if text_width > 0 else font_size
        
        # 重新加载字体
        try:
            for font_path in system_fonts:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, adjusted_font_size)
                    break
            if font is None:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # 重新计算文字大小
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else font.getsize(text)
        
        # 处理边距参数
        margin_bottom = margin_right = margin_left = margin_top = 20
        if isinstance(margins, dict):
            margin_bottom = margins.get('bottom', 20)
            margin_right = margins.get('right', 20)
            margin_top = margins.get('top', 20)
            margin_left = margins.get('left', 20)
        elif isinstance(margins, int):
            margin_bottom = margin_right = margin_top = margin_left = margins
        
        # 计算水印位置
        if position == 'top-left':
            position = (margin_left, margin_top)
        elif position == 'top-right':
            position = (width - text_width - margin_right, margin_top)
        elif position == 'bottom-left':
            position = (margin_left, height - text_height - margin_bottom)
        elif position == 'bottom-right':
            position = (width - text_width - margin_right, height - text_height - margin_bottom)
        elif position == 'center':
            position = ((width - text_width) // 2, (height - text_height) // 2)
        else:
            position = (width - text_width - margin_right, height - text_height - margin_bottom)  # 默认右下角
        
        # 如果设置了背景色
        if bg_color[3] > 0:  # 如果不是完全透明
            # 创建背景矩形
            rect_padding = 10  # 文字周围的内边距
            rect_position = (
                position[0] - rect_padding,
                position[1] - rect_padding,
                position[0] + text_width + rect_padding,
                position[1] + text_height + rect_padding
            )
            
            # 根据是否设置圆角决定绘制方式
            if corner_radius > 0:
                draw_rounded_rectangle(draw, rect_position, bg_color, corner_radius)
            else:
                draw.rectangle(rect_position, fill=bg_color)
        
        # 绘制文字
        draw.text(position, text, font=font, fill=font_color)
        
        # 合并图层
        result = Image.alpha_composite(image, txt)
        
        # 如果原图是RGB模式（没有透明通道），转回RGB模式
        if Image.open(input_path).mode == 'RGB':
            result = result.convert('RGB')
        
        # 保存结果
        result.save(output_path)
        print(f"已添加文字水印: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        return True
    except Exception as e:
        print(f"处理 {input_path} 时出错: {e}")
        return False

def add_watermark(input_path, output_path, watermark_path, position='bottom-right', margins=20, scale=0.2, text=None, font_size=40, font_color=(255, 255, 255, 128), bg_color=(0, 0, 0, 0), corner_radius=0):
    """
    给图片添加水印
    
    参数：
        input_path: 输入图片路径
        output_path: 输出图片路径
        watermark_path: 水印图片路径
        position: 水印位置，可选值：'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        margins: 水印边距，可以是整数（所有边距相同）或字典（指定不同方向的边距）
        scale: 水印缩放比例，0-1之间的小数
        text: 文字水印内容，如果指定则使用文字水印，忽略watermark_path
        font_size: 字体大小
        font_color: 字体颜色，RGBA格式
        bg_color: 水印背景颜色，RGBA格式
        corner_radius: 背景矩形的圆角半径（像素）
    """
    # 如果提供了文本，使用文字水印
    if text:
        return add_text_watermark(input_path, output_path, text, font_size, font_color, position, margins, scale, bg_color, corner_radius)
    
    try:
        # 打开原始图片
        image = Image.open(input_path).convert('RGBA')
        
        # 打开水印图片
        watermark = Image.open(watermark_path).convert('RGBA')
        
        # 计算水印的新尺寸
        width, height = image.size
        watermark_width, watermark_height = watermark.size
        new_width = int(width * scale)
        new_height = int(watermark_height * (new_width / watermark_width))
        
        # 调整水印大小
        watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
        
        # 处理边距参数
        margin_bottom = margin_right = margin_left = margin_top = 20
        if isinstance(margins, dict):
            margin_bottom = margins.get('bottom', 20)
            margin_right = margins.get('right', 20)
            margin_top = margins.get('top', 20)
            margin_left = margins.get('left', 20)
        elif isinstance(margins, int):
            margin_bottom = margin_right = margin_top = margin_left = margins
        
        # 计算水印位置
        if position == 'top-left':
            position = (margin_left, margin_top)
        elif position == 'top-right':
            position = (width - new_width - margin_right, margin_top)
        elif position == 'bottom-left':
            position = (margin_left, height - new_height - margin_bottom)
        elif position == 'bottom-right':
            position = (width - new_width - margin_right, height - new_height - margin_bottom)
        elif position == 'center':
            position = ((width - new_width) // 2, (height - new_height) // 2)
        else:
            position = (width - new_width - margin_right, height - new_height - margin_bottom)  # 默认右下角
        
        # 创建透明图层
        transparent = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # 调整水印图片的透明度
        if font_color[3] < 255:  # 使用font_color的透明度作为水印图片的透明度
            # 创建新的水印图片，应用透明度
            watermark_with_opacity = Image.new('RGBA', watermark.size, (0, 0, 0, 0))
            for x in range(watermark.width):
                for y in range(watermark.height):
                    r, g, b, a = watermark.getpixel((x, y))
                    # 应用新的透明度，保持原图像的透明度比例
                    new_a = int(a * font_color[3] / 255)
                    watermark_with_opacity.putpixel((x, y), (r, g, b, new_a))
            watermark = watermark_with_opacity
        
        # 如果设置了背景色
        if bg_color[3] > 0:  # 如果不是完全透明
            # 创建一个新的图层用于绘制背景
            bg_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(bg_layer)
            
            # 绘制背景矩形
            rect_padding = 10  # 水印周围的内边距
            rect_position = (
                position[0] - rect_padding,
                position[1] - rect_padding,
                position[0] + new_width + rect_padding,
                position[1] + new_height + rect_padding
            )
            
            # 根据是否设置圆角决定绘制方式
            if corner_radius > 0:
                draw_rounded_rectangle(draw, rect_position, bg_color, corner_radius)
            else:
                draw.rectangle(rect_position, fill=bg_color)
            
            # 将背景层合并到透明层
            transparent = Image.alpha_composite(transparent, bg_layer)
        # 如果设置了圆角但背景是透明的，可以为水印图片添加圆角效果
        elif corner_radius > 0:
            # 创建一个与水印大小相同的黑色背景和透明蒙版
            mask = Image.new('L', (new_width, new_height), 0)
            mask_draw = ImageDraw.Draw(mask)
            
            # 在蒙版上绘制圆角矩形
            rect_position = (0, 0, new_width, new_height)
            if corner_radius > min(new_width, new_height) // 2:
                corner_radius = min(new_width, new_height) // 2
                
            # 绘制圆角矩形蒙版
            if corner_radius > 0:
                # 绘制中间矩形
                mask_draw.rectangle((corner_radius, 0, new_width - corner_radius, new_height), fill=255)
                mask_draw.rectangle((0, corner_radius, new_width, new_height - corner_radius), fill=255)
                
                # 绘制四个圆角
                mask_draw.pieslice((0, 0, corner_radius * 2, corner_radius * 2), 180, 270, fill=255)
                mask_draw.pieslice((new_width - corner_radius * 2, 0, new_width, corner_radius * 2), 270, 0, fill=255)
                mask_draw.pieslice((0, new_height - corner_radius * 2, corner_radius * 2, new_height), 90, 180, fill=255)
                mask_draw.pieslice((new_width - corner_radius * 2, new_height - corner_radius * 2, new_width, new_height), 0, 90, fill=255)
            
            # 将蒙版应用到水印图片
            watermark.putalpha(mask)
        
        # 将水印粘贴到透明层
        transparent.paste(watermark, position, watermark)
        
        # 合并图层
        result = Image.alpha_composite(image, transparent)
        
        # 如果原图是RGB模式（没有透明通道），转回RGB模式
        if Image.open(input_path).mode == 'RGB':
            result = result.convert('RGB')
        
        # 保存结果
        result.save(output_path)
        print(f"已添加水印: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        return True
    except Exception as e:
        print(f"处理 {input_path} 时出错: {e}")
        return False

def process_directory(input_dir, output_dir, watermark_path=None, position='bottom-right', margins=20, scale=0.2, text=None, font_size=40, font_color=(255, 255, 255, 128), bg_color=(0, 0, 0, 0), corner_radius=0):
    """批量处理目录下的所有图片"""
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 支持的图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    # 统计信息
    total = 0
    successful = 0
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        # 跳过目录和不支持的文件格式
        if os.path.isdir(input_path):
            continue
        
        ext = os.path.splitext(filename)[1].lower()
        if ext not in image_extensions:
            continue
        
        total += 1
        output_path = os.path.join(output_dir, filename)
        
        # 添加水印
        if add_watermark(input_path, output_path, watermark_path, position, margins, scale, text, font_size, font_color, bg_color, corner_radius):
            successful += 1
    
    # 打印统计信息
    print(f"\n处理完成！")
    print(f"总计图片: {total}")
    print(f"成功处理: {successful}")
    print(f"失败数量: {total - successful}")
    print(f"处理后的图片保存在: {output_dir}")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量给图片添加水印')
    parser.add_argument('--input_dir', required=True, help='输入图片文件夹路径')
    parser.add_argument('--output_dir', required=True, help='输出图片文件夹路径')
    parser.add_argument('--watermark', help='水印图片路径')
    parser.add_argument('--text', help='文字水印内容')
    parser.add_argument('--font_size', type=int, default=40, help='文字水印字体大小')
    parser.add_argument('--position', default='bottom-right', 
                        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                        help='水印位置')
    parser.add_argument('--margin_bottom', type=int, default=20, help='水印距离底边的距离（像素）')
    parser.add_argument('--margin_right', type=int, default=20, help='水印距离右边的距离（像素）')
    parser.add_argument('--scale', type=float, default=0.2, help='水印缩放比例（相对于原图的宽度）')
    parser.add_argument('--opacity', type=int, default=128, help='水印透明度（0-255）')
    parser.add_argument('--bg_color', default='#000000', help='水印背景颜色（十六进制，如#FF0000）')
    parser.add_argument('--corner_radius', type=int, default=0, help='背景矩形的圆角半径（像素）')
    
    args = parser.parse_args()
    
    # 验证输入
    if not os.path.exists(args.input_dir):
        print(f"错误: 输入目录 '{args.input_dir}' 不存在")
        return
    
    if not args.text and not args.watermark:
        print(f"错误: 必须指定水印图片路径或文字水印内容")
        return
    
    if args.watermark and not os.path.exists(args.watermark):
        print(f"错误: 水印图片 '{args.watermark}' 不存在")
        return
    
    if args.scale <= 0 or args.scale > 1:
        print(f"警告: 缩放比例应在0-1之间，已自动调整为0.2")
        args.scale = 0.2
    
    # 处理背景颜色
    try:
        bg_hex = args.bg_color.lstrip('#')
        r = int(bg_hex[0:2], 16)
        g = int(bg_hex[2:4], 16)
        b = int(bg_hex[4:6], 16)
        bg_color = (r, g, b, args.opacity)
    except:
        print(f"警告: 无效的背景颜色格式，使用默认黑色")
        bg_color = (0, 0, 0, args.opacity)
    
    # 处理字体颜色（RGBA格式，半透明白色）
    font_color = (255, 255, 255, args.opacity)
    
    # 设置边距字典
    margins = {
        'bottom': args.margin_bottom,
        'right': args.margin_right
    }
    
    # 处理图片
    process_directory(args.input_dir, args.output_dir, args.watermark,
                     args.position, margins, args.scale, args.text, args.font_size, 
                     font_color, bg_color, args.corner_radius)

if __name__ == "__main__":
    main() 