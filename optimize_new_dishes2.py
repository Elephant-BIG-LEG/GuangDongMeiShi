#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新菜品图片优化脚本
"""

import os
from PIL import Image

def compress_image(input_path, output_path, max_width=600, quality=75):
    """压缩图片为WebP格式"""
    try:
        with Image.open(input_path) as img:
            width, height = img.size

            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)

            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            img.save(output_path, 'WEBP', quality=quality, method=6)

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = (1 - compressed_size / original_size) * 100

            print(f"  [OK] {original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB ({reduction:.1f}% 减少)")
            return True

    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return False

def main():
    dishes_dir = "assets/images/dishes"
    output_dir = os.path.join(dishes_dir, "optimized")

    # 新增的菜品图片
    new_dishes = [
        "广式烧鸭.png",
        "橙汁山药.jpg",
        "百花酿鱼肚.jpg",
        "酸甜咕噜肉.jpg"
    ]

    print(f"\n{'='*60}")
    print(f"优化新增菜品：{len(new_dishes)} 张")
    print(f"{'='*60}\n")

    success_count = 0
    for i, filename in enumerate(new_dishes, 1):
        input_path = os.path.join(dishes_dir, filename)
        output_filename = os.path.splitext(filename)[0] + '.webp'
        output_path = os.path.join(output_dir, output_filename)

        print(f"[{i}/{len(new_dishes)}] {filename}")
        if compress_image(input_path, output_path):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"优化完成！成功: {success_count}/{len(new_dishes)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()