"""Import the supplied fifth-edition textbook without modifying the source scan."""
from pathlib import Path
import argparse
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'management-operations-research'


def render_table_math(text):
    # Markdown does not parse inline math inside raw HTML tables.
    def table(match):
        return re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)',
                      lambda m: '<span class="arithmatex">\\(' + html.escape(m[1]) + '\\)</span>',
                      match[0], flags=re.S)
    return re.sub(r'<table\b.*?</table>', table, text, flags=re.S)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    source = args.source
    text = source.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    chapters = list(re.finditer(r'^# 第[一二三四五六七八九十]+章 (.+)$', text, re.M))
    appendix = re.search(r'^# 附录 .+$', text, re.M)
    references = re.search(r'^## 参考文献\s*$', text, re.M)
    assert len(chapters) == 17 and appendix and references
    target = ROOT / 'content/books' / SLUG
    assert not target.exists(), 'Existing book requires a reviewed update rather than reimport.'
    images = re.findall(r'!\[[^]]*\]\((images/[^)]+)\)', text)
    images += re.findall(r'<img\b[^>]*src=["\'](images/[^"\']+)', text)
    assert all((source.parent / name).is_file() for name in images)
    nav = []

    def write(rel, title, body, depth):
        body = re.sub(r'^#{1,4} +§\s*(\d+\.\d+)\s*', r'## \1 ', body, flags=re.M)
        body = re.sub(r'^### (案例\s*\d+[:：])', r'## \1', body, flags=re.M)
        # Keep captions out of the heading tree and explicitly center them.
        body = re.sub(r'^(附?图\s*\d+(?:\s*[-－—]\s*\d+)?(?:[^\n]*)?)$',
                      lambda m: '<p class="figure-caption">' + html.escape(m[1]) + '</p>', body, flags=re.M)
        body = body.replace('(images/', '(' + '../' * depth + 'images/')
        body = body.replace('src="images/', 'src="' + '../' * depth + 'images/')
        # Two set-builder bars in chapter 6 incorrectly open a second delimiter.
        body = body.replace(r'\left| d_{i1}^{\prime}', r'\middle| d_{i1}^{\prime}')
        body = render_table_math(body)
        # Isolate display delimiters from paragraphs for the site's Markdown renderer.
        body = re.sub(r'\n\$\$\n(.*?)\n\$\$\n', r'\n\n$$\n\1\n$$\n\n', body, flags=re.S)
        path = target / 'docs' / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body.strip() + '\n', encoding='utf-8')
        nav.append({title: rel})

    front = text[:chapters[0].start()]
    front = front.replace('# 管理运筹学（第5版）', '# 管理运筹学（第5版）\n\n主编：韩伯棠　｜　内容提供：周芸丽', 1)
    write('00-front-matter/index.md', '前置内容', front, 1)
    for i, chapter in enumerate(chapters, 1):
        end = chapters[i].start() if i < len(chapters) else appendix.start()
        title = f'第{i}章 {chapter[1]}'
        body = '# ' + title + '\n' + text[chapter.end():end]
        write(f'chapters/{i:02}/index.md', title, body, 2)
    write('appendices/index.md', '附录：软件 3.5 版使用说明', text[appendix.start():references.start()], 1)
    write('references/index.md', '参考文献与配套资源说明', '# 参考文献与配套资源说明\n\n' + text[references.start():], 1)
    for name in set(images):
        destination = target / 'docs' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source.parent / name, destination)
    import yaml
    (target / 'mkdocs.yml').write_text(yaml.safe_dump({'site_name': '管理运筹学（第5版）', 'docs_dir': 'docs', 'nav': nav}, allow_unicode=True, sort_keys=False), encoding='utf-8')
    config_path = ROOT / 'books.json'
    config_text = config_path.read_text(encoding='utf-8')
    category = {'id': 'management-science', 'title': '管理科学与运筹优化', 'eyebrow': 'MANAGEMENT SCIENCE', 'description': '学习运筹建模、优化方法与管理决策。'}
    book = {'slug': SLUG, 'title': '管理运筹学（第5版）', 'author': '韩伯棠 主编', 'contentProvider': '周芸丽', 'description': '涵盖线性规划、整数规划、动态规划、网络模型、存储论、排队论、对策论、决策分析与预测。', 'tags': ['运筹学', '优化建模', '管理决策'], 'category': 'management-science', 'type': 'reference'}
    assert SLUG not in config_text and '"management-science"' not in config_text
    config_text = config_text.replace('"categories": [', '"categories": [\n' + '      ' + json.dumps(category, ensure_ascii=False) + ',', 1)
    config_text = config_text.replace('"books": [', '"books": [\n    ' + json.dumps(book, ensure_ascii=False) + ',', 1)
    json.loads(config_text)
    config_path.write_text(config_text, encoding='utf-8')
    print(f'Imported {len(nav)} documents, {len(set(images))} images; original source unchanged.')


if __name__ == '__main__':
    main()
