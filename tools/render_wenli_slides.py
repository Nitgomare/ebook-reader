"""Read-only native PowerPoint export using late binding."""
import json
from pathlib import Path
from win32com.client import dynamic

ROOT=Path(__file__).resolve().parents[1]
jobs=json.loads((ROOT/'tmp/wenli-slide-job.json').read_text(encoding='utf-8'))
app=dynamic.Dispatch('PowerPoint.Application')
try:
    for job in jobs:
        dest=Path(job['destination']); dest.mkdir(parents=True,exist_ok=True)
        deck=app.Presentations.Open(job['source'],-1,0,0)
        try:
            for n in range(1,deck.Slides.Count+1):
                target=dest/f'{n:04}.jpg'
                if not target.exists():
                    deck.Slides.Item(n).Export(str(target),'JPG',1600,int(1600*deck.PageSetup.SlideHeight/deck.PageSetup.SlideWidth))
            print(job['id'],deck.Slides.Count,'slides',flush=True)
        finally: deck.Close()
finally: app.Quit()
