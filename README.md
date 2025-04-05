# 批量图片添加水印

这个Python脚本可以批量给指定文件夹下的所有图片添加水印。

## 功能

- 支持批量处理同一文件夹下的所有图片
- 支持两种水印类型：图片水印和文字水印
- 可以自定义文字水印的内容、大小和颜色
- 可以调整水印文字和图片的透明度
- 可以自定义背景色并应用与水印相同的透明度
- 可以设置水印背景的圆角效果
- 对于图片水印，可以应用圆角效果
- 可以设置水印的大小和位置
- 支持精确调整水印的底边距和右边距（对于右下角位置）
- 处理后的图片保存在新的文件夹中，不影响原图
- 提供直观的十六进制颜色输入和预览

## 使用方法

### 一键启动（推荐）

我们提供了几种一键启动的方式，可以在任意位置启动水印工具：

- **Windows用户**：双击运行 `start_watermark.bat` 文件
- **macOS/Linux用户**：双击或在终端中运行 `start_watermark.sh` 文件
  - 首次使用前需要添加执行权限：`chmod +x start_watermark.sh`
- **所有平台**：通过Python运行 `python start_watermark.py`

这些启动脚本会自动处理路径问题，找到并启动水印工具的图形界面。

![image](https://github.com/user-attachments/assets/7d88da8b-7633-4283-9990-5a4f87aa5012)
![image](https://github.com/user-attachments/assets/5b5d3ec6-1fcf-4351-a0b2-ced670413e62)

### 命令行版本

1. 安装依赖：
```
pip install -r requirements.txt
```

2. 运行脚本：
```
python watermark.py [选项]
```

### 图形界面版本

```
python watermark_gui.py
```

图形界面提供了以下功能：
- 选择输入和输出文件夹
- 选择水印类型（图片水印或文字水印）
- 对于图片水印：
  - 选择水印图片
  - 设置圆角效果
- 对于文字水印：
  - 设置水印文字内容
  - 调整字体大小
  - 设置字体颜色（包括十六进制色值输入）
  - 设置背景色（包括十六进制色值输入）
- 水印透明度：
  - 调整水印文字或图片的透明度（0-100%）
  - 背景颜色将使用相同的透明度
- 水印位置设置：
  - 选择水印在图片中的位置（左上角、右上角、左下角、右下角、中心）
  - 精确调整底边距和右边距（对于右下角位置）
- 设置圆角半径（适用于文字水印背景和图片水印）
- 调整水印位置和大小
- 预览水印效果
- 批量处理，并显示进度

## 命令行参数说明

- `--input_dir`: 输入图片文件夹路径
- `--output_dir`: 输出图片文件夹路径
- `--watermark`: 水印图片路径（使用图片水印时需要）
- `--text`: 文字水印内容（使用文字水印时需要）
- `--font_size`: 文字水印字体大小，默认为40
- `--position`: 水印位置，可选值：'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
- `--margin_bottom`: 水印距离图片底边的距离（像素）
- `--margin_right`: 水印距离图片右边的距离（像素）
- `--scale`: 水印缩放比例，0-1之间的小数
- `--opacity`: 水印透明度，0-255，255表示完全不透明
- `--bg_color`: 水印背景颜色，十六进制格式，如 #000000 表示黑色
- `--corner_radius`: 水印背景矩形或图片水印的圆角半径，单位为像素

## 示例

### 添加图片水印：
```
python watermark.py --input_dir ./images --output_dir ./watermarked --watermark ./logo.png --position bottom-right --margin_bottom 20 --margin_right 20 --scale 0.2 --opacity 255 --corner_radius 10
```

### 添加文字水印：
```
python watermark.py --input_dir ./images --output_dir ./watermarked --text "版权所有" --position bottom-right --margin_bottom 20 --margin_right 20 --scale 0.2 --font_size 40 --opacity 255
```

### 添加带背景色的文字水印：
```
python watermark.py --input_dir ./images --output_dir ./watermarked --text "版权所有" --position bottom-right --margin_bottom 20 --margin_right 20 --scale 0.2 --bg_color "#000000" --opacity 255
```

### 添加带圆角背景的文字水印：
```
python watermark.py --input_dir ./images --output_dir ./watermarked --text "版权所有" --position bottom-right --margin_bottom 20 --margin_right 20 --scale 0.2 --bg_color "#000000" --opacity 255 --corner_radius 10
```

## 自动适应文字大小

程序会自动调整文字大小，确保水印文字不会超出设定的缩放比例。例如，如果缩放比例设为0.2，则水印文字最大宽度将限制在图片宽度的20%以内。

## 水印透明度

透明度值范围为0-255，其中0表示完全透明，255表示完全不透明。GUI中显示为百分比形式，更直观易用（0%表示完全不透明，100%表示完全透明）。设置的透明度会同时应用到水印文字/图片和背景色上。

## 颜色设置

GUI中提供了直观的颜色选择器，以及十六进制色值输入框，用户可以：
- 通过调色板选择颜色
- 直接输入十六进制色值（例如 #F3F3F3）并应用
- 颜色的显示和输入都在同一行，操作更加便捷

## 圆角效果

通过设置圆角半径，可以让水印呈现圆角效果：
- 对于文字水印，圆角应用于背景矩形
- 对于图片水印，圆角直接应用于水印图片本身
圆角半径为0时显示为普通矩形或原始图片，值越大圆角越明显。

## 精确控制水印位置

对于右下角位置，可以分别设置底边距和右边距，使水印的位置调整更加精确和灵活。

## 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- GIF
- WEBP 
