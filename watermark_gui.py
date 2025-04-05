#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageTk
import threading
from watermark import add_watermark

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("批量图片添加水印工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置变量
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.watermark_path = tk.StringVar()
        self.position = tk.StringVar(value="bottom-right")
        self.margin_bottom = tk.IntVar(value=20)  # 底边距
        self.margin_right = tk.IntVar(value=20)   # 右边距
        self.scale = tk.DoubleVar(value=0.2)
        self.preview_image = None
        self.watermark_type = tk.StringVar(value="image")
        self.watermark_text = tk.StringVar(value="水印文字")
        self.font_size = tk.IntVar(value=40)
        
        # 颜色相关变量
        self.font_color = (255, 255, 255, 255)  # RGBA，默认完全不透明
        self.font_color_display = tk.StringVar(value="#FFFFFF")
        self.font_r = tk.IntVar(value=255)
        self.font_g = tk.IntVar(value=255)
        self.font_b = tk.IntVar(value=255)
        
        self.bg_color = (0, 0, 0, 255)  # 默认完全不透明
        self.bg_color_display = tk.StringVar(value="#000000")
        self.bg_r = tk.IntVar(value=0)
        self.bg_g = tk.IntVar(value=0)
        self.bg_b = tk.IntVar(value=0)
        
        # 透明度 - 0-100%，与实际Alpha值0-255相反
        self.opacity_percent = tk.IntVar(value=0)  # 默认0%透明（完全不透明）
        self.opacity = 255  # 实际Alpha值，0-255
        self.corner_radius = tk.IntVar(value=0)  # 圆角半径
        
        # UI元素引用
        self.type_frame = None
        self.image_watermark_frame = None
        self.text_watermark_frame = None
        self.bg_color_frame = None
        self.opacity_frame = None
        self.corner_radius_frame = None
        self.button_frame = None
        
        # 创建UI
        self.create_widgets()
        
        # 位置选项
        self.position_options = {
            "左上角": "top-left",
            "右上角": "top-right",
            "左下角": "bottom-left",
            "右下角": "bottom-right",
            "中心": "center"
        }
        
        # 更新UI初始状态
        self.update_ui_for_watermark_type()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
        settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 输入目录
        input_frame = ttk.Frame(settings_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="输入文件夹:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.input_dir).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(input_frame, text="浏览...", command=self.select_input_dir).pack(side=tk.LEFT)
        
        # 输出目录
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="输出文件夹:").pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_dir).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="浏览...", command=self.select_output_dir).pack(side=tk.LEFT)
        
        # 水印类型选择
        self.type_frame = ttk.Frame(settings_frame)
        self.type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.type_frame, text="水印类型:").pack(side=tk.LEFT)
        ttk.Radiobutton(self.type_frame, text="图片水印", variable=self.watermark_type, value="image", 
                       command=self.update_ui_for_watermark_type).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.type_frame, text="文字水印", variable=self.watermark_type, value="text", 
                       command=self.update_ui_for_watermark_type).pack(side=tk.LEFT, padx=5)
        
        # 文字水印设置框
        self.text_watermark_frame = ttk.Frame(settings_frame)
        text_input_frame = ttk.Frame(self.text_watermark_frame)
        text_input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(text_input_frame, text="水印文字:").pack(side=tk.LEFT)
        self.text_entry = ttk.Entry(text_input_frame, textvariable=self.watermark_text)
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 字体大小
        font_size_frame = ttk.Frame(self.text_watermark_frame)
        font_size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_size_frame, text="字体大小:").pack(side=tk.LEFT)
        font_size_entry = tk.Spinbox(font_size_frame, from_=10, to=100, textvariable=self.font_size, width=10)
        font_size_entry.pack(side=tk.LEFT, padx=5)
        
        # 字体颜色和十六进制色值在同一行
        font_color_frame = ttk.Frame(self.text_watermark_frame)
        font_color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_color_frame, text="字体颜色:").pack(side=tk.LEFT)
        self.font_color_display_label = tk.Label(font_color_frame, bg="#FFFFFF", width=3, height=1)
        self.font_color_display_label.pack(side=tk.LEFT, padx=5)
        self.font_hex_entry = ttk.Entry(font_color_frame, textvariable=self.font_color_display, width=8)
        self.font_hex_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(font_color_frame, text="选择颜色", command=self.select_font_color).pack(side=tk.LEFT)
        ttk.Button(font_color_frame, text="应用", command=lambda: self.update_color_from_hex('font')).pack(side=tk.LEFT, padx=5)
        
        # 背景色设置和十六进制色值在同一行
        self.bg_color_frame = ttk.Frame(settings_frame)
        self.bg_color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.bg_color_frame, text="背景色:").pack(side=tk.LEFT)
        self.bg_color_display_label = tk.Label(self.bg_color_frame, bg="#000000", width=3, height=1)
        self.bg_color_display_label.pack(side=tk.LEFT, padx=5)
        self.bg_hex_entry = ttk.Entry(self.bg_color_frame, textvariable=self.bg_color_display, width=8)
        self.bg_hex_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.bg_color_frame, text="选择颜色", command=self.select_bg_color).pack(side=tk.LEFT)
        ttk.Button(self.bg_color_frame, text="应用", command=lambda: self.update_color_from_hex('bg')).pack(side=tk.LEFT, padx=5)
        
        # 水印透明度
        self.opacity_frame = ttk.Frame(settings_frame)
        self.opacity_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.opacity_frame, text="水印透明度:").pack(side=tk.LEFT)
        opacity_scale = ttk.Scale(self.opacity_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 variable=self.opacity_percent, command=self.update_opacity)
        opacity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.opacity_label = ttk.Label(self.opacity_frame, text="0%")
        self.opacity_label.pack(side=tk.LEFT)
        
        # 圆角设置
        self.corner_radius_frame = ttk.Frame(settings_frame)
        self.corner_radius_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.corner_radius_frame, text="圆角半径:").pack(side=tk.LEFT)
        corner_radius_entry = tk.Spinbox(self.corner_radius_frame, from_=0, to=50, textvariable=self.corner_radius, width=10)
        corner_radius_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.corner_radius_frame, text="像素").pack(side=tk.LEFT)
        
        # 图片水印选择框
        self.image_watermark_frame = ttk.Frame(settings_frame)
        ttk.Label(self.image_watermark_frame, text="水印图片:").pack(side=tk.LEFT)
        ttk.Entry(self.image_watermark_frame, textvariable=self.watermark_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(self.image_watermark_frame, text="浏览...", command=self.select_watermark).pack(side=tk.LEFT)
        
        # 位置选择
        position_frame = ttk.Frame(settings_frame)
        position_frame.pack(fill=tk.X, pady=5)
        ttk.Label(position_frame, text="水印位置:").pack(side=tk.LEFT)
        position_combo = ttk.Combobox(position_frame, textvariable=self.position)
        position_combo['values'] = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
        position_combo['state'] = 'readonly'
        position_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 底边距和右边距设置
        margin_frame = ttk.Frame(settings_frame)
        margin_frame.pack(fill=tk.X, pady=5)
        
        # 底边距
        ttk.Label(margin_frame, text="底边距:").pack(side=tk.LEFT)
        margin_bottom_entry = tk.Spinbox(margin_frame, from_=0, to=200, textvariable=self.margin_bottom, width=10)
        margin_bottom_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(margin_frame, text="像素").pack(side=tk.LEFT)
        
        # 右边距
        ttk.Label(margin_frame, text="右边距:").pack(side=tk.LEFT, padx=(10, 0))
        margin_right_entry = tk.Spinbox(margin_frame, from_=0, to=200, textvariable=self.margin_right, width=10)
        margin_right_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(margin_frame, text="像素").pack(side=tk.LEFT)
        
        # 缩放比例
        scale_frame = ttk.Frame(settings_frame)
        scale_frame.pack(fill=tk.X, pady=5)
        ttk.Label(scale_frame, text="缩放比例:").pack(side=tk.LEFT)
        scale_entry = tk.Spinbox(scale_frame, from_=0.01, to=1.0, increment=0.01, textvariable=self.scale, width=10)
        scale_entry.pack(side=tk.LEFT, padx=5)
        
        # 预览和运行按钮
        self.button_frame = ttk.Frame(settings_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(self.button_frame, text="预览效果", command=self.preview_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="批量处理", command=self.process_images).pack(side=tk.LEFT, padx=5)
        
        # 右侧预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="预览", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.preview_canvas = tk.Canvas(preview_frame, bg="white")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # 初始化透明度显示
        self.update_opacity()
    
    def update_opacity(self, *args):
        """更新透明度标签和实际透明度值"""
        percent = self.opacity_percent.get()
        self.opacity_label.config(text=f"{percent}%")
        
        # 计算实际透明度值 (反转逻辑：100%透明 = alpha 0, 0%透明 = alpha 255)
        self.opacity = int(255 * (100 - percent) / 100)
        
        # 更新字体颜色的透明度
        r, g, b, _ = self.font_color
        self.font_color = (r, g, b, self.opacity)
        
        # 更新背景颜色的透明度（如果已设置）
        if self.bg_color[3] > 0:
            r, g, b, _ = self.bg_color
            self.bg_color = (r, g, b, self.opacity)
            
        # 更新显示的颜色
        # 字体颜色
        r = self.font_r.get()
        g = self.font_g.get()
        b = self.font_b.get()
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.font_color_display_label.config(bg=hex_color)
        
        # 背景颜色
        r = self.bg_r.get()
        g = self.bg_g.get()
        b = self.bg_b.get()
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.bg_color_display_label.config(bg=hex_color)
    
    def update_ui_for_watermark_type(self):
        """根据水印类型更新UI显示"""
        if self.watermark_type.get() == "image":
            # 显示图片水印设置，隐藏文字水印设置
            self.image_watermark_frame.pack(fill=tk.X, pady=5, after=self.type_frame)
            self.text_watermark_frame.pack_forget()
            
            # 隐藏背景色设置，但保留圆角设置
            self.bg_color_frame.pack_forget()
            self.corner_radius_frame.pack(fill=tk.X, pady=5, after=self.opacity_frame)
        else:
            # 显示文字水印设置，隐藏图片水印设置
            self.image_watermark_frame.pack_forget()
            self.text_watermark_frame.pack(fill=tk.X, pady=5, after=self.type_frame)
            
            # 显示背景色设置和圆角设置
            self.bg_color_frame.pack(fill=tk.X, pady=5, after=self.opacity_frame)
            self.corner_radius_frame.pack(fill=tk.X, pady=5, after=self.bg_color_frame)
        
        # 无论是什么水印类型，都确保预览和批量处理按钮可见
        self.button_frame.pack(fill=tk.X, pady=10)
    
    def select_font_color(self):
        """选择字体颜色"""
        color = colorchooser.askcolor(title="选择字体颜色", initialcolor="#FFFFFF")
        if color[1]:  # 如果用户选择了颜色
            hex_color = color[1]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            # 更新RGB变量
            self.font_r.set(r)
            self.font_g.set(g)
            self.font_b.set(b)
            
            # 更新颜色显示
            self.font_color_display_label.config(bg=hex_color)
            
            # 更新十六进制值
            self.font_color_display.set(hex_color)
            
            # 存储RGBA颜色
            self.font_color = (r, g, b, self.opacity)
    
    def select_bg_color(self):
        """选择背景颜色"""
        color = colorchooser.askcolor(title="选择背景颜色", initialcolor="#000000")
        if color[1]:  # 如果用户选择了颜色
            hex_color = color[1]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            # 更新RGB变量
            self.bg_r.set(r)
            self.bg_g.set(g)
            self.bg_b.set(b)
            
            # 更新颜色显示
            self.bg_color_display_label.config(bg=hex_color)
            
            # 更新十六进制值
            self.bg_color_display.set(hex_color)
            
            # 存储RGBA颜色
            self.bg_color = (r, g, b, self.opacity)
    
    def select_input_dir(self):
        dir_path = filedialog.askdirectory(title="选择输入图片文件夹")
        if dir_path:
            self.input_dir.set(dir_path)
            # 自动设置输出目录
            self.output_dir.set(os.path.join(os.path.dirname(dir_path), "watermarked"))
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出图片文件夹")
        if dir_path:
            self.output_dir.set(dir_path)
    
    def select_watermark(self):
        file_path = filedialog.askopenfilename(
            title="选择水印图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")]
        )
        if file_path:
            self.watermark_path.set(file_path)
    
    def preview_watermark(self):
        # 检查输入
        if not self.validate_inputs(preview=True):
            return
        
        # 获取第一张图片进行预览
        image_files = []
        for filename in os.listdir(self.input_dir.get()):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']:
                image_files.append(os.path.join(self.input_dir.get(), filename))
                break
        
        if not image_files:
            messagebox.showinfo("提示", "输入文件夹中没有图片文件")
            return
        
        # 创建临时目录
        temp_dir = os.path.join(os.path.dirname(image_files[0]), ".temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        else:
            # 清除上一次的预览
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
        
        # 生成预览图
        temp_output = os.path.join(temp_dir, "preview.png")
        
        watermark_type = self.watermark_type.get()
        
        # 处理不同的水印类型
        if watermark_type == "image":
            watermark_path = self.watermark_path.get()
            text = None
            # 图片水印不使用背景色，但支持圆角
            bg_color = (0, 0, 0, 0)
            corner_radius = self.corner_radius.get()
        else:
            watermark_path = None
            text = self.watermark_text.get()
            bg_color = self.bg_color
            corner_radius = self.corner_radius.get()
        
        # 获取水印位置对应的边距
        margins = self.get_position_margins()
        
        result = add_watermark(
            image_files[0], 
            temp_output, 
            watermark_path,
            self.position.get(),
            margins,
            self.scale.get(),
            text,
            self.font_size.get(),
            self.font_color,
            bg_color,
            corner_radius
        )
        
        if result:
            # 显示预览图
            self.display_preview(temp_output)
            self.status_var.set("预览生成成功")
        else:
            messagebox.showerror("错误", "预览生成失败")
            self.status_var.set("预览生成失败")
    
    def get_position_margins(self):
        """根据位置返回合适的边距"""
        position = self.position.get()
        if position == "bottom-right":
            return {
                "bottom": self.margin_bottom.get(),
                "right": self.margin_right.get()
            }
        else:
            # 对于其他位置，暂时返回一个统一的边距值
            # 注意：后续可以扩展此功能，为每个位置提供独立的边距调整
            return self.margin_bottom.get()
    
    def display_preview(self, image_path):
        try:
            # 打开图片
            img = Image.open(image_path)
            
            # 调整图片大小以适应画布
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width <= 1:  # 如果画布尚未完全初始化
                canvas_width = 300
                canvas_height = 300
            
            # 计算缩放比例
            img_width, img_height = img.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # 缩放图片
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 转换为Tkinter可用的格式
            photo_img = ImageTk.PhotoImage(img)
            
            # 保存引用以防止垃圾回收
            self.preview_image = photo_img
            
            # 清除画布并显示图片
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                canvas_width // 2, canvas_height // 2,
                image=photo_img, anchor=tk.CENTER
            )
            
        except Exception as e:
            messagebox.showerror("错误", f"无法显示预览: {e}")
    
    def validate_inputs(self, preview=False):
        # 检查输入目录
        if not self.input_dir.get() or not os.path.exists(self.input_dir.get()):
            messagebox.showerror("错误", "请选择有效的输入文件夹")
            return False
        
        watermark_type = self.watermark_type.get()
        
        # 检查水印图片或文字
        if watermark_type == "image":
            if not self.watermark_path.get() or not os.path.exists(self.watermark_path.get()):
                messagebox.showerror("错误", "请选择有效的水印图片")
                return False
        else:  # text
            if not self.watermark_text.get():
                messagebox.showerror("错误", "请输入水印文字")
                return False
        
        # 预览模式不检查输出目录
        if not preview:
            # 检查输出目录
            if not self.output_dir.get():
                messagebox.showerror("错误", "请选择输出文件夹")
                return False
            
            # 创建输出目录（如果不存在）
            if not os.path.exists(self.output_dir.get()):
                try:
                    os.makedirs(self.output_dir.get())
                except Exception as e:
                    messagebox.showerror("错误", f"无法创建输出文件夹: {e}")
                    return False
        
        # 检查底边距和右边距是否为非负数
        try:
            margin_bottom = self.margin_bottom.get()
            margin_right = self.margin_right.get()
            if margin_bottom < 0 or margin_right < 0:
                messagebox.showerror("错误", "边距必须大于或等于0")
                return False
        except:
            messagebox.showerror("错误", "边距必须是有效的数字")
            return False
        
        # 检查缩放比例是否在有效范围
        try:
            scale = self.scale.get()
            if scale <= 0 or scale > 1:
                messagebox.showerror("错误", "缩放比例必须在0-1之间")
                return False
        except:
            messagebox.showerror("错误", "缩放比例必须是有效的数字")
            return False
        
        # 检查圆角半径是否为非负数
        try:
            radius = self.corner_radius.get()
            if radius < 0:
                messagebox.showerror("错误", "圆角半径必须大于或等于0")
                return False
        except:
            messagebox.showerror("错误", "圆角半径必须是有效的数字")
            return False
        
        return True
    
    def process_images(self):
        # 验证输入
        if not self.validate_inputs():
            return
        
        # 在新线程中处理图片，避免界面冻结
        self.status_var.set("正在处理...")
        threading.Thread(target=self._process_images_thread).start()
    
    def _process_images_thread(self):
        try:
            input_dir = self.input_dir.get()
            output_dir = self.output_dir.get()
            watermark_type = self.watermark_type.get()
            
            # 处理不同的水印类型
            if watermark_type == "image":
                watermark_path = self.watermark_path.get()
                text = None
                # 图片水印不使用背景色，但支持圆角
                bg_color = (0, 0, 0, 0)
                corner_radius = self.corner_radius.get()
            else:
                watermark_path = None
                text = self.watermark_text.get()
                bg_color = self.bg_color
                corner_radius = self.corner_radius.get()
            
            position = self.position.get()
            margins = self.get_position_margins()
            scale = self.scale.get()
            font_size = self.font_size.get()
            font_color = self.font_color
            
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 支持的图片格式
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
            
            # 获取所有图片文件
            image_files = []
            for filename in os.listdir(input_dir):
                input_path = os.path.join(input_dir, filename)
                if os.path.isdir(input_path):
                    continue
                ext = os.path.splitext(filename)[1].lower()
                if ext in image_extensions:
                    image_files.append((filename, input_path))
            
            # 统计信息
            total = len(image_files)
            successful = 0
            failed = 0
            
            # 更新进度条范围
            self.progress_var.set(0)
            
            # 处理每个图片
            for i, (filename, input_path) in enumerate(image_files):
                # 更新状态
                self.status_var.set(f"处理中: {i+1}/{total} - {filename}")
                
                output_path = os.path.join(output_dir, filename)
                
                # 添加水印
                if add_watermark(input_path, output_path, watermark_path, position, margins, scale, text, font_size, font_color, bg_color, corner_radius):
                    successful += 1
                else:
                    failed += 1
                
                # 更新进度条
                progress = (i + 1) / total * 100
                self.progress_var.set(progress)
                
                # 更新UI
                self.root.update_idletasks()
            
            # 完成处理
            self.status_var.set(f"处理完成！成功: {successful}, 失败: {failed}")
            messagebox.showinfo("完成", f"图片处理完成！\n成功: {successful}\n失败: {failed}\n处理后的图片保存在: {output_dir}")
            
        except Exception as e:
            self.status_var.set(f"处理出错: {e}")
            messagebox.showerror("错误", f"处理过程中发生错误: {e}")
    
    def update_color_from_hex(self, color_type):
        """根据十六进制颜色值更新颜色"""
        try:
            if color_type == 'font':
                hex_color = self.font_color_display.get().lstrip('#')
                if len(hex_color) != 6:
                    messagebox.showerror("错误", "请输入有效的六位十六进制颜色值，例如 F3F3F3")
                    return
                    
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # 更新RGB变量
                self.font_r.set(r)
                self.font_g.set(g)
                self.font_b.set(b)
                
                # 更新颜色显示
                self.font_color_display_label.config(bg=f"#{hex_color}")
                
                # 存储RGBA颜色
                self.font_color = (r, g, b, self.opacity)
                
            elif color_type == 'bg':
                hex_color = self.bg_color_display.get().lstrip('#')
                if len(hex_color) != 6:
                    messagebox.showerror("错误", "请输入有效的六位十六进制颜色值，例如 F3F3F3")
                    return
                    
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # 更新RGB变量
                self.bg_r.set(r)
                self.bg_g.set(g)
                self.bg_b.set(b)
                
                # 更新颜色显示
                self.bg_color_display_label.config(bg=f"#{hex_color}")
                
                # 存储RGBA颜色
                self.bg_color = (r, g, b, self.opacity)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的十六进制颜色值，例如 F3F3F3")

    def update_color_from_rgb(self, color_type):
        """根据RGB值更新颜色"""
        if color_type == 'font':
            r = self.font_r.get()
            g = self.font_g.get()
            b = self.font_b.get()
            
            # 更新字体颜色
            self.font_color = (r, g, b, self.opacity)
            
            # 更新颜色显示
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.font_color_display_label.config(bg=hex_color)
            self.font_color_display.set(hex_color)
        elif color_type == 'bg':
            r = self.bg_r.get()
            g = self.bg_g.get()
            b = self.bg_b.get()
            
            # 更新背景颜色
            self.bg_color = (r, g, b, self.opacity)
            
            # 更新颜色显示
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_color_display_label.config(bg=hex_color)
            self.bg_color_display.set(hex_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop() 