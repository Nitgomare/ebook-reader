"""Import Wenli's Markdown courses and prepare slide previews without publishing video."""
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent.parent / '扫描书籍/文丽'
COURSES = [('abb-lab', 'ABB机器人实验台实验指导书', 'ABB机器人实验台实验指导书'),
           ('aimibot-education', '教育机器人教材', '教育机器人教材.pdf-')]

def main():
    config = json.loads((ROOT/'books.json').read_text(encoding='utf-8'))
    jobs = []
    for slug, title, prefix in COURSES:
        folder = next(p for p in SOURCE.iterdir() if p.is_dir() and p.name.startswith(prefix))
        source_md = folder/'full.md'
        if not source_md.exists(): source_md = next(folder.glob('*.md'))
        book = ROOT/'content/books'/slug
        docs = book/'docs'
        docs.mkdir(parents=True, exist_ok=True)
        text = source_md.read_text(encoding='utf-8-sig')
        headings = list(re.finditer(r'^#{1,2}\s+(第\s*[一二三四五六七八九十百\d]+\s*章[^\n]*)$', text, re.M))
        nav = [{'前言与目录':'front/index.md'}]
        pieces = [('front/index.md', text[:headings[0].start()])]
        for i, match in enumerate(headings):
            label = re.sub(r'\s+', ' ', match[1]).strip()
            path = f'chapters/{i+1:02}/index.md'
            nav.append({label:path})
            pieces.append((path, text[match.start():headings[i+1].start() if i+1<len(headings) else len(text)]))
        for rel, body in pieces:
            dest = docs/rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            body = body.replace('images/', '../../images/' if rel.startswith('chapters/') else '../images/')
            dest.write_text(body, encoding='utf-8')
        shutil.copytree(folder/'images', docs/'images', dirs_exist_ok=True)
        if slug == 'aimibot-education':
            supplements = []
            order = {'二':2,'四':4,'五':5,'六':6,'八':8,'十':10}
            for lab in SOURCE.iterdir():
                if not lab.is_dir() or not (lab/'full.md').exists() or not lab.name.startswith('实验'): continue
                name = lab.name.split('.pdf-')[0].strip()
                number = order[re.match(r'实验([二四五六八十])',name)[1]]
                rel = f'experiments/{number:02}/index.md'
                dest = docs/rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text((lab/'full.md').read_text(encoding='utf-8-sig'),encoding='utf-8')
                shutil.copytree(lab/'images',dest.parent/'images',dirs_exist_ok=True)
                supplements.append((number,{name:rel}))
            nav.append({'补充实验':[entry for _,entry in sorted(supplements)]})
            associations={2:4,4:5,5:5,6:6,8:7,10:3}
            for number, entry in sorted(supplements):
                name, rel = next(iter(entry.items()))
                chapter=associations[number]
                chapter_path=docs/f'chapters/{chapter:02}/index.md'
                with chapter_path.open('a',encoding='utf-8') as stream:
                    stream.write(f'\n\n## 配套补充实验\n\n[{name}](../../{rel})\n')
            decks = []
            topics={
                'aimibot_Introduction':('Aimibot 机器人介绍',[1]),
                'aimibot_System installation':('软件系统安装',[4]),
                'aimibot_course_1':('移动机器人基础操作',[3,4]),
                'aimibot_course_2':('移动机器人运动控制',[5]),
                'aimibot_course_3':('移动机器人轨迹控制与避障',[5,6]),
                'aimibot_course_4':('移动机器人激光建图与导航',[7,8]),
                'aimibot_course_8&9':('移动机器人激光建图、导航与避障',[6,7,8]),
                'aimibot_course_10':('视觉跟踪乒乓球实验',[]),
                'aimibot_course_11':('视觉与激光雷达融合导航与避障',[7,8]),
                '进阶实验-三角形运动、超声波跟随':('进阶实验：三角形运动、超声波跟随',[5,6]),
            }
            for ppt in sorted(SOURCE.glob('*.pptx')):
                digest = hashlib.sha256(ppt.read_bytes()).hexdigest()[:16]
                with zipfile.ZipFile(ppt) as archive:
                    pages = sorted([n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)],key=lambda n:int(re.search(r'slide(\d+)',n)[1]))
                    texts = [' '.join(t.text or '' for t in ET.fromstring(archive.read(n)).findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t')) for n in pages]
                topic, chapters=topics[ppt.stem]
                deck = {'id':digest,'title':topic,'chapters':chapters,'topic':topic,'pageCount':len(pages),'variant':'配套课件','sources':[ppt.name]}
                decks.append(deck)
                jobs.append({'source':str(ppt),'id':digest,'destination':str(ROOT/'tmp/wenli-slide-render'/digest)})
                (ROOT/'tmp/wenli-slide-render').mkdir(parents=True,exist_ok=True)
                (ROOT/'tmp/wenli-slide-render'/f'{digest}.txt').write_text('\n'.join(texts),encoding='utf-8')
            slides = book/'slides'
            slides.mkdir(exist_ok=True)
            (slides/'manifest.json').write_text(json.dumps({'title':title+' · 文丽老师配套课件','decks':decks},ensure_ascii=False,indent=2),encoding='utf-8')
        (book/'mkdocs.yml').write_text(yaml.safe_dump({'site_name':title,'docs_dir':'docs','nav':nav},allow_unicode=True,sort_keys=False),encoding='utf-8')
        if not any(b['slug']==slug for b in config['books']):
            config['books'].append({'slug':slug,'title':title,'author':'文丽老师提供','description':'机器人实验台装置、仿真、示教编程与综合应用实验。' if slug=='abb-lab' else 'Aimibot ROS 教育机器人教材，配套六份补充实验和在线授课课件。','tags':['ABB','实验指导'] if slug=='abb-lab' else ['ROS','Aimibot','实验与课件'],'category':'robotics','type':'course'})
        next(b for b in config['books'] if b['slug']==slug)['compactResources']=True
        print(title,len(headings),'chapters')
    (ROOT/'books.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'tmp/wenli-slide-job.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')

def finalize():
    slides=ROOT/'content/books/aimibot-education/slides'
    manifest=json.loads((slides/'manifest.json').read_text(encoding='utf-8'))
    for deck in manifest['decks']:
        dest=slides/deck['id']; dest.mkdir(exist_ok=True)
        for n in range(1,deck['pageCount']+1):
            with Image.open(ROOT/'tmp/wenli-slide-render'/deck['id']/f'{n:04}.jpg') as img:
                img.save(dest/f'{n:04}.webp',quality=85,method=4)
    print(len(manifest['decks']),'decks',sum(d['pageCount'] for d in manifest['decks']),'slides')

if __name__=='__main__':
    import sys
    finalize() if '--finalize' in sys.argv else main()
