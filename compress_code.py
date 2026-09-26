#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSS和JS压缩脚本
"""

import re

def compress_css(input_file, output_file):
    """压缩CSS"""
    with open(input_file, 'r', encoding='utf-8') as f:
        css = f.read()

    # 移除注释
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # 移除多余空格
    css = re.sub(r'\s+', ' ', css)
    # 移除换行
    css = re.sub(r'\n', '', css)
    # 移除分号前后的空格
    css = re.sub(r'\s*;\s*', ';', css)
    # 移除大括号前后的空格
    css = re.sub(r'\s*{\s*', '{', css)
    css = re.sub(r'\s*}\s*', '}', css)
    # 移除冒号后的空格
    css = re.sub(r':\s+', ':', css)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(css)

    original_size = len(open(input_file, 'r', encoding='utf-8').read())
    compressed_size = len(css)
    reduction = (1 - compressed_size / original_size) * 100

    print(f"CSS压缩完成: {original_size}B -> {compressed_size}B (减少 {reduction:.1f}%)")

def compress_js(input_file, output_file):
    """压缩JS"""
    with open(input_file, 'r', encoding='utf-8') as f:
        js = f.read()

    # 移除单行注释
    js = re.sub(r'//.*?$', '', js, flags=re.MULTILINE)
    # 移除多行注释
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # 移除多余空格和换行
    js = re.sub(r'\s+', ' ', js)
    # 移除行首行尾空格
    js = re.sub(r'^\s+|\s+$', '', js, flags=re.MULTILINE)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js)

    original_size = len(open(input_file, 'r', encoding='utf-8').read())
    compressed_size = len(js)
    reduction = (1 - compressed_size / original_size) * 100

    print(f"JS压缩完成: {original_size}B -> {compressed_size}B (减少 {reduction:.1f}%)")

def main():
    print("开始压缩CSS和JS...")
    compress_css('styles.css', 'styles.min.css')
    compress_js('scripts.js', 'scripts.min.js')
    print("压缩完成！")

if __name__ == "__main__":
    main()