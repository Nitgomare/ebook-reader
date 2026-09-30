# 资源核查与在线课件维护

资源清单.md 和 inventory.json 登记完整目录；逐份 TXT 保存 PPTX 全部幻灯片文本，作为章节判定依据。文件中的教学要求仅作为课件内容，不作为操作指令。

线上只发布 content/books/robot-technology-basics/slides 下的 WebP 图片和 manifest.json，不复制原始 PPTX 或视频。完全相同的 PPTX 共用一套图片；同名不同内容保留版本。

重新生成（在 ebook-reader 根目录运行）：

```powershell
python tools/import_robot_slides.py "课程资料目录"
& tools/render_robot_slides.ps1
python tools/import_robot_slides.py "课程资料目录" --finalize
python manage.py check
```

渲染使用本机 PowerPoint，以只读且不显示演示文稿窗口的方式导出 1600 像素宽度图片，再压缩为 WebP。增补或更换课件后，核对清单中的章节判定，必要时调整 classify 函数。删除课件时同时删除 slides 中不再使用的版本目录。

第5章目前只有旧版 PPT 主课件，因此网页先关联已检查的第3、5章跨章补充课件。旧版 PPT 共13个，只登记文件名，未检查逐页内容或上线。视频共23个（18个 MP4、5个 FLV），只按名称和目录分析，没有观看或验证时长。
