"""Generate local PPT/PDF previews with read-only native export.

Add PPTX or PDF files to the research presentation extra-resources directory, then run
this script before build.py. Existing previews are reused by content hash.

PDF decks are rendered with PyMuPDF, PPTX decks with desktop PowerPoint.
"""
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import quote

import pymupdf
from PIL import Image
from win32com.client import dynamic

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'content/books/research-skills'
SOURCE = BOOK / 'docs/07-research-presentation/extra-resources'
DEST = BOOK / 'slides'
PAGE_WIDTH = 1600
PROVIDERS = {
    '大小微模型赋能先进制造：实践与思考': '戴琼',
    '特高压换流站中性线电流零磁通测量技术与装置': '戴琼',
    '大型风电齿轮箱关键技术': '戴琼',
}


def clean_title(stem):
    title = re.sub(r'\(1\)$', '', stem)
    if title == 'PPT复刻':
        title = 'PPT 复刻案例'
    return title


def category_for(source, title):
    if source.stem.startswith('框架'):
        return '汇报框架'
    if any(key in title for key in ('齿轮箱', '换流站', '特高压')):
        return '工程技术'
    return '科研案例'


def download_url(source):
    path = source.relative_to(BOOK / 'docs').as_posix()
    return '/'.join(quote(part) for part in ('files', 'research-skills', *path.split('/')))


def render_pdf(source, target, count):
    target.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(source)
    for page_no in range(1, count + 1):
        output = target / f'{page_no:04}.webp'
        if output.exists():
            continue
        page = document[page_no - 1]
        zoom = PAGE_WIDTH / page.rect.width
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        with Image.open(io.BytesIO(pixmap.tobytes('png'))) as image:
            image.convert('RGB').save(output, 'WEBP', quality=86)


def build_pdf_deck(source):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    count = pymupdf.open(source).page_count
    target = DEST / digest
    render_pdf(source, target, count)
    title = clean_title(source.stem)
    with Image.open(target / '0001.webp') as cover:
        width, height = cover.size
    return dict(id=digest, title=title, pageCount=count, category=category_for(source, title),
                width=width, height=height, chapters=[], variant='扩展资源', sources=[source.name],
                format='PDF', provider=PROVIDERS.get(title),
                size=source.stat().st_size, downloadUrl=download_url(source))


def build_pptx_deck(app_holder, source):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    with zipfile.ZipFile(source) as archive:
        count = sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml', name)) for name in archive.namelist())
    target = DEST / digest
    target.mkdir(parents=True, exist_ok=True)
    if any(not (target / f'{page:04}.webp').exists() for page in range(1, count + 1)):
        if not app_holder:
            app_holder.append(dynamic.Dispatch('PowerPoint.Application'))
        presentation = app_holder[0].Presentations.Open(str(source), -1, 0, 0)
        try:
            for page in range(1, count + 1):
                output = target / f'{page:04}.webp'
                if output.exists():
                    continue
                temp = ROOT / 'tmp/ppt-library-render' / digest / f'{page:04}.png'
                temp.parent.mkdir(parents=True, exist_ok=True)
                presentation.Slides.Item(page).Export(str(temp), 'PNG', PAGE_WIDTH,
                                                   int(PAGE_WIDTH * presentation.PageSetup.SlideHeight / presentation.PageSetup.SlideWidth))
                with Image.open(temp) as image:
                    image.convert('RGB').save(output, 'WEBP', quality=86)
        finally:
            presentation.Close()
    title = clean_title(source.stem)
    with Image.open(target / '0001.webp') as cover:
        width, height = cover.size
    return dict(id=digest, title=title, pageCount=count, category=category_for(source, title),
                width=width, height=height, chapters=[], variant='扩展资源', sources=[source.name],
                format='PPTX', provider=PROVIDERS.get(title),
                size=source.stat().st_size, downloadUrl=download_url(source))


def main():
    decks = []
    app_holder = []
    try:
        for source in sorted(SOURCE.glob('*.pptx')) + sorted(SOURCE.glob('*.pdf')):
            if source.name.startswith('~$'):
                continue
            deck = build_pdf_deck(source) if source.suffix.lower() == '.pdf' else build_pptx_deck(app_holder, source)
            print(f"{deck['title']}: {deck['pageCount']} pages ({deck['format']})", flush=True)
            same = next((d for d in decks if d['title'] == deck['title']), None)
            if same is not None:
                # Same deck delivered twice: keep one card and offer both files.
                same.setdefault('extraDownloads', []).append(dict(
                    name=source.name, format=deck['format'], size=deck['size'],
                    provider=deck['provider'], downloadUrl=deck['downloadUrl']))
                print(f'  -> merged into existing card "{same["title"]}" as extra download', flush=True)
                continue
            decks.append(deck)
    finally:
        if app_holder:
            app_holder[0].Quit()
    # Publish the manifest only after every preview is ready.
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'manifest.json').write_text(json.dumps(dict(title='PPT 资源库', decks=decks), ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
