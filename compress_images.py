#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片批量压缩脚本
将菜品图片压缩到合理大小，提升网页加载速度
"""

import os
import glob
from PIL import Image

def compress_image(input_path, output_path, max_width=800, quality=85):
    """
    压缩图片
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_width: 最大宽度（像素）
        quality: JPEG质量（1-100）
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 获取原始尺寸
            width, height = img.size

            # 如果宽度大于max_width，按比例缩小
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                print(f"  尺寸调整: {width}x{height} -> {max_width}x{new_height}")

            # 转换为RGB模式（如果是RGBA或其他模式）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # 保存为JPEG
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

            # 计算压缩比例
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = (1 - compressed_size / original_size) * 100

            print(f"  [OK] 压缩完成: {original_size/1024/1024:.2f}MB -> {compressed_size/1024:.1f}KB (减少 {reduction:.1f}%)")
            return True

    except Exception as e:
        print(f"  [ERROR] 压缩失败: {str(e)}")
        return False

def main():
    """主函数"""
    # 图片目录
    dishes_dir = "assets/images/dishes"

    # 创建输出目录
    output_dir = os.path.join(dishes_dir, "compressed")
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有图片文件
    image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(dishes_dir, ext)))

    # 过滤掉已压缩的图片
    image_files = [f for f in image_files if 'compressed' not in f]

    print(f"\n{'='*60}")
    print(f"找到 {len(image_files)} 张图片待压缩")
    print(f"{'='*60}\n")

    success_count = 0
    fail_count = 0

    for i, image_path in enumerate(image_files, 1):
        filename = os.path.basename(image_path)
        # 统一使用.jpg扩展名
        output_filename = os.path.splitext(filename)[0] + '.jpg'
        output_path = os.path.join(output_dir, output_filename)

        print(f"[{i}/{len(image_files)}] 处理: {filename}")

        if compress_image(image_path, output_path):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{'='*60}")
    print(f"压缩完成！")
    print(f"  成功: {success_count} 张")
    print(f"  失败: {fail_count} 张")
    print(f"  输出目录: {output_dir}")
    print(f"{'='*60}\n")

    # 计算总大小
    total_original = sum(os.path.getsize(f) for f in image_files)
    compressed_files = glob.glob(os.path.join(output_dir, '*.jpg'))
    total_compressed = sum(os.path.getsize(f) for f in compressed_files)

    print(f"原始总大小: {total_original/1024/1024:.2f}MB")
    print(f"压缩后总大小: {total_compressed/1024/1024:.2f}MB")
    print(f"总共减少: {(1 - total_compressed/total_original)*100:.1f}%")

if __name__ == "__main__":
    main()