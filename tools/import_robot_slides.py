"""Audit local teaching materials and prepare a native PowerPoint rendering job.

Usage: python tools/import_robot_slides.py SOURCE_DIRECTORY
Inspect legacy PPT with inspect_legacy_robot_slides.ps1, then run
render_robot_slides.ps1 and this script with --finalize. selection.json
controls the published chapters; all original resources remain in the audit.
Original presentations, videos and unrelated files are never published.
"""
import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'content/books/robot-technology-basics'
NAMES = {1:'绪论',2:'机器人本体结构',3:'机器人运动学',4:'机器人动力学',5:'机器人轨迹规划',6:'机器人控制系统',7:'机器人语言与编程',8:'工业机器人',9:'操纵型机器人',10:'仿生机器人'}

def classify(path):
    name = path.name
    if '离线编程' in name: return [7], '第7章补充：离线编程基础认知'
    if '智能机器人' in name: return [], '拓展：智能机器人（旧版第10章，与第三版第10章仿生机器人不同）'
    if '附录' in name: return [], '附录：机器人课程实验示例'
    if '运动学与轨迹规划' in name: return [3,5], '第3、5章补充：运动学与轨迹规划（ER16实例）'
    if '第1-2' in name: return [1], '第1章 绪论（含课程介绍）'
    if '第3-4' in name: return [2], '第2章 机器人本体结构'
    m = re.match(r'(\d+)\s', name)
    if m and int(m[1]) in NAMES:
        n = int(m[1]); return [n], f'第{n}章 {NAMES[n]}'
    return [], '待人工核对'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--finalize', action='store_true')
    args = parser.parse_args()
    source = args.source.resolve()
    audit = ROOT / 'resource-inventory/robot-technology-basics'
    audit.mkdir(parents=True, exist_ok=True)
    assets = BOOK / 'slides'
    assets.mkdir(exist_ok=True)
    files, decks, hashes = [], [], {}
    for p in sorted(source.rglob('*')):
        if not p.is_file(): continue
        rel = p.relative_to(source).as_posix()
        item = {'path':rel,'bytes':p.stat().st_size,'extension':p.suffix.lower()}
        files.append(item)
        if p.suffix.lower() != '.pptx': continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        with zipfile.ZipFile(p) as z:
            pages = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)),key=lambda n:int(re.search(r'slide(\d+)',n)[1]))
            texts = [' '.join(t.text or '' for t in ET.fromstring(z.read(n)).findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t')).rstrip() for n in pages]
            links = [n for n in z.namelist() if n.startswith('ppt/slides/_rels/') and b'TargetMode="External"' in z.read(n)]
        chapters, topic = classify(p)
        deck = {**item,'id':digest[:16],'sha256':digest,'title':p.stem,'chapters':chapters,'topic':topic,'pageCount':len(texts),'evidence':texts[:6],'externalLinkSlides':len(links),'duplicateOf':hashes.get(digest),'variant':'公开课' if '公开课' in rel else ('素材参考' if '素材/' in rel else ('最后一节课版本' if '最后一节课' in rel else '授课资料'))}
        hashes.setdefault(digest,rel)
        decks.append(deck)
        (audit / (digest[:16]+'.txt')).write_text('\n\n'.join(f'第{i}页\n{t}' for i,t in enumerate(texts,1))+'\n',encoding='utf-8')
    videos = [f for f in files if f['extension'] in {'.mp4','.flv','.avi','.wmv','.mov','.mkv'}]
    for v in videos:
        path = v['path']
        v['analysis'] = ('绪论/机器人应用演示' if '第1次课' in path else '本体结构/减速器演示' if '第2-3次课' in path else '第5章轨迹规划演示' if '第五章' in path else '课程回顾/机器人性能与应用') + '（仅按目录和文件名推断，未观看）'
        v['sameNameGroup'] = Path(path).stem
    report = {'source':str(source),'files':files,'presentations':decks,'videos':videos,'counts':dict(Counter(f['extension'] for f in files))}
    (audit/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines = ['# 机器人技术基础授课资源清单','',f'来源：`{source}`','',f'共 {len(files)} 个文件；{len(decks)} 个 PPTX，{len(hashes)} 个独立内容版本；{len(videos)} 个视频文件。','', '## PPTX 与教材章节对应','', '依据逐页提取的文本、封面和目录判定；同名文件保留版本区别。完整逐页文本见同目录 TXT。','', '| 相对路径 | 页数 | 对应内容 | 版本/重复 |','|---|---:|---|---|']
    for d in decks: lines.append(f"| {d['path']} | {d['pageCount']} | {d['topic']} | {d['variant']}" + (f"；完全重复于 {d['duplicateOf']}" if d['duplicateOf'] else '') + ' |')
    lines += ['', '## 视频清单（不上传）','','仅分析文件名；相同名称的 MP4/FLV 或不同目录副本不代表已验证内容一致。','','| 相对路径 | MB | 文件名推断 |','|---|---:|---|']
    lines += [f"| {v['path']} | {v['bytes']/1024**2:.2f} | {v['analysis']} |" for v in videos]
    lines += ['', '## 其他文件','','旧版 PPT 目前只登记文件名，未转换在线课件。采购合同、安装程序、网页片段与素材图片仅列入本地资源清单。','','| 相对路径 | 类型 | MB |','|---|---|---:|']
    lines += [f"| {f['path']} | {f['extension']} | {f['bytes']/1024**2:.2f} |" for f in files if f['extension'] != '.pptx' and f not in videos]
    lines += ['', '## 核对结论','','- 第5章主课件只有旧版 PPT；目前第5章提供跨章的运动学与轨迹规划 PPTX 补充。','- 最后一节课的《10 智能机器人》属于旧版/拓展内容，不归入第三版第10章《仿生机器人》。','- 第四章文件夹的《机器人的运动学与轨迹规划》实际对应第3、5章，不能按所在文件夹归为动力学。','- 同名但哈希不同的课件保留为不同版本；完全重复的课件共用线上页面。','- 网页以静态幻灯片展示，保留原版式；动画、音视频和原有超链接交互不执行。']
    (audit/'资源清单.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    selection_path = audit / 'selection.json'
    unique = [d for d in decks if not d['duplicateOf']]
    if selection_path.is_file():
        selection = json.loads(selection_path.read_text(encoding='utf-8'))
        legacy_path = audit / 'legacy-ppt-review.json'
        legacy = json.loads(legacy_path.read_text(encoding='utf-8-sig')) if legacy_path.is_file() else []
        by_path = {d['path']:d for d in decks}
        for entry in legacy:
            original = source / entry['path']
            if hashlib.sha256(original.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError(f"Legacy PPT changed; rerun inspect_legacy_robot_slides.ps1: {entry['path']}")
            by_path[entry['path']] = {**entry, 'chapters':[], 'topic':'旧版课件', 'variant':'授课资料', 'duplicateOf':None}
        unique = []
        for chosen in selection['decks']:
            if chosen['path'] not in by_path:
                raise ValueError(f"Selected file not inspected: {chosen['path']}")
            deck = dict(by_path[chosen['path']])
            n = chosen['chapter']
            deck.update(chapters=[n], topic=f'第{n}章 {NAMES[n]}', title=f'第{n}章 {NAMES[n]}', variant='主课件', selectionReason=chosen['reason'])
            unique.append(deck)
        if sorted(d['chapters'][0] for d in unique) != list(range(1,11)):
            raise ValueError('Selection must contain exactly one deck for each chapter 1–10')
        report['legacyPresentations'] = [{k:v for k,v in d.items() if k != 'pages'} for d in legacy]
        report['onlineSelection'] = [{'chapter':d['chapters'][0], 'path':d['path'], 'pageCount':d['pageCount'], 'reason':d['selectionReason']} for d in unique]
        (audit/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        for entry in legacy:
            (audit/(entry['id']+'.txt')).write_text('\n\n'.join(f'第{i}页\n'+ '\n'.join(line.strip() for line in t.splitlines()) for i,t in enumerate(entry['pages'],1)).rstrip()+'\n',encoding='utf-8')
        selection_lines = ['# 在线主课件筛选说明','',selection['policy'],'',f"原网站19份独立版本、987页；现选择10份主课件、{sum(d['pageCount'] for d in unique)}页。精简课件入口，不删改原始幻灯片。",'', '| 章节 | 来源 | 页数 | 选择依据 |','|---|---|---:|---|']
        selection_lines += [f"| {d['topic']} | {d['path']} | {d['pageCount']} | {d['selectionReason']} |" for d in unique]
        selection_lines += ['', '未选课件保留在本地完整资源清单和逐页文本中，不在网站发布。视频仍只登记文件名。旧版13个PPT已通过PowerPoint逐页提取文本，第5章主课件新增在线渲染。']
        (audit/'主课件筛选说明.md').write_text('\n'.join(selection_lines)+'\n',encoding='utf-8')
        lines = [line.replace('旧版 PPT 目前只登记文件名，未转换在线课件。','旧版 PPT 已通过 PowerPoint 提取逐页文本，主课件选择见主课件筛选说明.md。').replace('- 第5章主课件只有旧版 PPT；目前第5章提供跨章的运动学与轨迹规划 PPTX 补充。','- 第5章采用55页《第5章--机器人轨迹规划.ppt》作为主课件，撤下ER16跨章补充。') for line in lines]
        lines += ['', '## 当前线上主课件','','网站已精简为每章一份，共10份；来源、内容比较及排除理由见[主课件筛选说明](主课件筛选说明.md)。']
        (audit/'资源清单.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    job = [{'source':str(source/d['path']),'id':d['id'],'destination':str((ROOT/'tmp/robot-slide-render'/d['id']).resolve())} for d in unique]
    (audit/'render-job.json').write_text(json.dumps(job,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.finalize:
        from PIL import Image
        for d in unique:
            dest = assets/d['id']; dest.mkdir(exist_ok=True)
            for i in range(1,d['pageCount']+1):
                if (dest/f'{i:04}.webp').is_file(): continue
                jpg = ROOT/'tmp/robot-slide-render'/d['id']/f'{i:04}.jpg'
                with Image.open(jpg) as im: im.save(dest/f'{i:04}.webp',quality=85,method=4)
        manifest = {'title':'机器人技术基础 · 肖钊授课主课件','decks':[{k:d[k] for k in ('id','title','chapters','topic','pageCount','variant')} | {'sources':[d['path']]} for d in unique]}
        (assets/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(files)} files, {len(decks)} PPTX, {len(unique)} online decks, {sum(d["pageCount"] for d in unique)} slides, {len(videos)} videos')

if __name__ == '__main__': main()
