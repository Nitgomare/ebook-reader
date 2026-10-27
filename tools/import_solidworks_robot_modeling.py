"""Import the SolidWorks course and preserve its authored landing page."""
from pathlib import Path
import argparse
import json
import re
import shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'solidworks-robot-modeling'
TITLE = '基于 SolidWorks 的智能机器人建模'
HOME = 'solidworks_based_geometric_modeling_of_intelligent_robots.md'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    source = parser.parse_args().source.resolve()
    target = ROOT / 'content/books' / SLUG
    assert not target.exists(), 'Review existing content before replacing this course.'
    docs = target / 'docs'
    docs.mkdir(parents=True)
    files = sorted(source.rglob('*.md'))
    assert len(files) == 9
    chapters = sorted([p for p in files if p.name != HOME], key=lambda p: int(p.parent.name.split('_')[0]))
    links = [p.relative_to(source).as_posix() for p in chapters]
    nav = [{'课程首页与学习导航': HOME}]
    images = set()
    for path in [source / HOME, *chapters]:
        rel = path.relative_to(source)
        text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
        text = text.replace('> 主编:  何志鹏  龙东平  马文悦  邓越平\n> >湖南科技大学机电工程学院\n> \n>2026年10月',
                            '> 主编：何志鹏、龙东平、马文悦、邓越平  \n> 湖南科技大学机电工程学院 · 2026年10月')
        if path.name == HOME:
            text = '# ' + TITLE + '\n\n' + text
            quick = '\n\n[开始学习：第1章](' + links[0] + ') · [查看目录与资源](#/resources/' + SLUG + ')\n\n'
            text = text.replace('## 引言', quick + '## 引言', 1)
        else:
            i = chapters.index(path) + 1
            match = re.match(r'# 第[一二三四五六七八]章 (.+)', text)
            assert match
            title = f'第{i}章 {match[1]}'
            text = '# ' + title + text[match.end():]
            nav.append({title: rel.as_posix()})
        if path.parent.name.startswith('2_'):
            # The supplied unnumbered image is the eDrawings viewer shown in §2.4.
            text = text.replace('pic2/pic.2.9.jpg', 'pic2/8ac57447dd0696a35c76d5edfe87a032.jpg')
            text = text.replace('下&emsp;&emsp;图是', '&emsp;&emsp;下图是').replace('右侧工具栏提供了', '工具栏提供了')
        # The site's stylesheet already indents paragraphs.
        text = text.replace('&emsp;&emsp;', '')
        def autolink(match):
            url = match[0].rstrip('.,;')
            return '<' + url + '>' + match[0][len(url):]
        text = re.sub(r'(?<![\w(<"\'])https?://[^\s<>，。；）]+', autolink, text)
        for name in re.findall(r'!\[[^]]*\]\(([^)]+)\)', text):
            image = path.parent / name
            assert image.is_file(), image
            images.add(image)
        out = docs / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text.strip() + '\n', encoding='utf-8')
    for image in images:
        out = docs / image.relative_to(source)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image, out)
    (target / 'mkdocs.yml').write_text(yaml.safe_dump({'site_name': TITLE, 'docs_dir': 'docs', 'nav': nav}, allow_unicode=True, sort_keys=False), encoding='utf-8')
    book = {'slug': SLUG, 'title': TITLE, 'author': '何志鹏、龙东平、马文悦、邓越平 主编',
            'description': '湖南科技大学智能机器人设计与控制微专业教材，从 SolidWorks 基础操作与复杂零件建模，逐步完成智能小车、机械手爪和机械臂的几何建模与装配。',
            'tags': ['SolidWorks', '几何建模', '机器人装配'], 'category': 'robotics', 'type': 'course',
            'coverSource': 'pic0/pic.0.0.jpg', 'homePage': HOME}
    config = ROOT / 'books.json'
    raw = config.read_text(encoding='utf-8')
    assert SLUG not in raw
    raw = raw.replace('"books": [', '"books": [\n    ' + json.dumps(book, ensure_ascii=False) + ',', 1)
    json.loads(raw)
    config.write_text(raw, encoding='utf-8')
    print(f'Imported {len(nav)} pages and {len(images)} unique images; homepage preserved.')


if __name__ == '__main__':
    main()
