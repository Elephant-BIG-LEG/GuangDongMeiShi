#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片深度压缩脚本 - WebP格式 + 更小尺寸
目标：将图片减少到1MB以内
"""

import os
import glob
from PIL import Image

def compress_to_webp(input_path, output_path, max_width=600, quality=75):
    """
    压缩图片为WebP格式
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_width: 最大宽度（像素）- 降低到600px
        quality: WebP质量（1-100）- 降低到75
    """
    try:
        with Image.open(input_path) as img:
            width, height = img.size

            # 缩小尺寸
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # 转换为RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # 保存为WebP
            img.save(output_path, 'WEBP', quality=quality, method=6)

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = (1 - compressed_size / original_size) * 100

            print(f"  [OK] {original_size/1024/1024:.2f}MB -> {compressed_size/1024:.1f}KB ({reduction:.1f}% 减少)")
            return True

    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return False

def main():
    dishes_dir = "assets/images/dishes"
    output_dir = os.path.join(dishes_dir, "optimized")
    os.makedirs(output_dir, exist_ok=True)

    # 只处理compressed目录中的图片（已经压缩过的）
    compressed_dir = os.path.join(dishes_dir, "compressed")
    image_files = glob.glob(os.path.join(compressed_dir, '*.jpg'))

    print(f"\n{'='*60}")
    print(f"深度优化：{len(image_files)} 张图片")
    print(f"格式：WebP | 尺寸：600px | 质量：75")
    print(f"{'='*60}\n")

    success_count = 0
    for i, image_path in enumerate(image_files, 1):
        filename = os.path.basename(image_path)
        output_filename = os.path.splitext(filename)[0] + '.webp'
        output_path = os.path.join(output_dir, output_filename)

        print(f"[{i}/{len(image_files)}] {filename}")
        if compress_to_webp(image_path, output_path):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"优化完成！成功: {success_count}/{len(image_files)}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*60}\n")

    # 统计
    total_compressed = sum(os.path.getsize(f) for f in image_files)
    optimized_files = glob.glob(os.path.join(output_dir, '*.webp'))
    total_optimized = sum(os.path.getsize(f) for f in optimized_files)

    print(f"压缩前: {total_compressed/1024/1024:.2f}MB")
    print(f"优化后: {total_optimized/1024/1024:.2f}MB")
    print(f"总减少: {(1 - total_optimized/total_compressed)*100:.1f}%")

if __name__ == "__main__":
    main()