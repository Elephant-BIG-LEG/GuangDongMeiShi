#!/bin/bash
# 清理原始图片脚本 - 只保留优化后的WebP图片

echo "开始清理原始图片..."
echo "=================="

# 删除菜品原始图片
cd assets/images/dishes
rm -f *.jpg *.png 2>/dev/null
echo "✓ 已删除菜品原始图片"

# 删除压缩中间文件
rm -rf compressed 2>/dev/null
echo "✓ 已删除compressed目录"

# 删除环境原始图片
cd ../environment
rm -f *.jpg *.png 2>/dev/null
echo "✓ 已删除环境原始图片"

echo "=================="
echo "清理完成！"
echo "只保留优化后的WebP图片"