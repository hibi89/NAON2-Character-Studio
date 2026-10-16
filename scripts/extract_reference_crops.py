"""Exact-pixel NAON2 concept-sheet crops for reference only, NOT master drawings."""
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'assets/references/naon2-character-sheet-v1.png'
out=ROOT/'assets/derivatives/reference-crops-v02'
out.mkdir(parents=True,exist_ok=True)
boxes={
 'turnaround-front':(24,466,216,685),
 'turnaround-side':(219,466,400,685),
 'turnaround-back':(399,466,581,685),
 'expression-neutral':(617,470,713,565),
 'expression-smile':(720,470,817,565),
 'expression-surprised':(830,470,928,565),
 'expression-curious':(939,470,1036,565),
 'expression-wink':(1050,470,1147,565),
}
im=Image.open(src).convert('RGB')
assert im.size==(1536,1024), im.size
for name,rect in boxes.items():
 im.crop(rect).save(out/(name+'.png'))
 print(name,rect)
