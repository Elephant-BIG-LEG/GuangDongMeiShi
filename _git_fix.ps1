Remove-Item 'D:\GuangDongMeiShi\.git\index.lock' -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
git -C 'D:\GuangDongMeiShi' add -f assets/ .gitignore
git -C 'D:\GuangDongMeiShi' commit -m '添加图片和视频'
git -C 'D:\GuangDongMeiShi' push
Write-Host 'Done'
