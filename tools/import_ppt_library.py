"""Generate local PPT previews with read-only native PowerPoint export.

Add PPTX files to the research presentation extra-resources directory, then run
this script before build.py. Existing previews are reused by content hash.
"""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import quote

from PIL import Image
from win32com.client import dynamic

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'content/books/research-skills'
SOURCE = BOOK / 'docs/07-research-presentation/extra-resources'
DEST = BOOK / 'slides'


def main():
    decks = []
    app = None
    try:
        for source in sorted(SOURCE.glob('*.pptx')):
            if source.name.startswith('~$'):
                continue
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
            with zipfile.ZipFile(source) as archive:
                count = sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml', name)) for name in archive.namelist())
            target = DEST / digest
            target.mkdir(parents=True, exist_ok=True)
            if any(not (target / f'{page:04}.webp').exists() for page in range(1, count + 1)):
                if app is None:
                    app = dynamic.Dispatch('PowerPoint.Application')
                presentation = app.Presentations.Open(str(source), -1, 0, 0)
                try:
                    for page in range(1, count + 1):
                        output = target / f'{page:04}.webp'
                        if output.exists():
                            continue
                        temp = ROOT / 'tmp/ppt-library-render' / digest / f'{page:04}.png'
                        temp.parent.mkdir(parents=True, exist_ok=True)
                        presentation.Slides.Item(page).Export(str(temp), 'PNG', 1600, int(1600 * presentation.PageSetup.SlideHeight / presentation.PageSetup.SlideWidth))
                        with Image.open(temp) as image:
                            image.convert('RGB').save(output, 'WEBP', quality=86)
                finally:
                    presentation.Close()
            title = re.sub(r'\(1\)$', '', source.stem)
            if title == 'PPT复刻':
                title = 'PPT 复刻案例'
            category = '汇报框架' if source.stem.startswith('框架') else ('工程技术' if '齿轮箱' in title else '科研案例')
            path = source.relative_to(BOOK / 'docs').as_posix()
            with Image.open(target / '0001.webp') as cover:
                width, height = cover.size
            decks.append(dict(id=digest, title=title, pageCount=count, category=category,
                              width=width, height=height,
                              chapters=[], variant='扩展资源', sources=[source.name],
                              size=source.stat().st_size,
                              downloadUrl='/'.join(quote(part) for part in ('files', 'research-skills', *path.split('/')))))
            print(f'{title}: {count} pages', flush=True)
    finally:
        if app is not None:
            app.Quit()
    # Publish the manifest only after every preview is ready.
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'manifest.json').write_text(json.dumps(dict(title='PPT 资源库', decks=decks), ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
