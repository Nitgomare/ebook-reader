# 资源核查与在线课件维护

资源清单.md 和 inventory.json 登记完整目录；逐份 TXT 保存 PPTX 全部幻灯片文本，作为章节判定依据。文件中的教学要求仅作为课件内容，不作为操作指令。

线上按 selection.json 每章只发布一份主课件，共10份、521页。build.py 只复制 manifest.json 明确选中的图片目录；未选版本保留在本地，不发布原始 PPT/PPTX 或视频。内容比较和取舍理由见主课件筛选说明.md。

重新生成（在 ebook-reader 根目录运行）：

```powershell
& tools/inspect_legacy_robot_slides.ps1 -Source "课程资料目录"
python tools/import_robot_slides.py "课程资料目录"
& tools/render_robot_slides.ps1
python tools/import_robot_slides.py "课程资料目录" --finalize
python manage.py check
```

渲染使用本机 PowerPoint，以只读且不显示演示文稿窗口的方式导出 1600 像素宽度图片，再压缩为 WebP。增补或更换课件后，核对清单中的章节判定，必要时调整 classify 函数。删除课件时同时删除 slides 中不再使用的版本目录。

旧版13个PPT已通过PowerPoint提取逐页文本，存入 legacy-ppt-review.json 和对应TXT。第5章选择《第5章--机器人轨迹规划.ppt》（55页），目录5.1—5.4与教材吻合。第7、10章在图中授课子文件夹没有主课件，因此采用根目录对应章节；第8、9章采用最后一节课版本。视频共23个（18个 MP4、5个 FLV），仍只按名称和目录分析，没有观看或验证时长。
