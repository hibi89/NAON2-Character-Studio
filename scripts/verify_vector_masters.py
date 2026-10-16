#!/usr/bin/env python3
"""Validate NAON2 draft SVG source and rendered PNGs; excludes visual likeness approval."""
from pathlib import Path
import hashlib, json
from PIL import Image
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/masters/vector-v01'
items=[]
for view in ('front','side','back'):
    svg=OUT/f'naon2-{view}-vector-master-v01.svg'
    png=OUT/f'naon2-{view}-vector-master-v01.png'
    root=ET.parse(svg).getroot()
    paths=len(root.findall('.//{http://www.w3.org/2000/svg}path'))
    assert paths>=10, (view,paths)
    assert not root.findall('.//{http://www.w3.org/2000/svg}image'), 'Embedded raster forbidden'
    with Image.open(png) as im:
        im.load()
        assert im.size==(2048,2048) and im.mode=='RGBA'
        assert im.getpixel((0,0))[3]==0 and im.getpixel((2047,2047))[3]==0
        bbox=im.getbbox()
        assert bbox and bbox[0]>200 and bbox[2]<1930 and bbox[1]>240 and bbox[3]<1950, (view,bbox)
        items.append({'view':view,'dimensions':list(im.size),'paths':paths,'visible_bounds':bbox,'svg_sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'png_bytes':png.stat().st_size,'status':'DRAFT, VISUAL USER APPROVAL REQUIRED'})
(OUT/'qa-manifest.json').write_text(json.dumps({'project':'NAON2','kind':'original editable SVG redraw + 2K vector-render PNG','note':'2K output is a vector rendering, not a 2K copy of the original raster illustration. User likeness approval and legal review pending.','items':items},ensure_ascii=False,indent=2)+'\n')
for item in items: print('PASS',item['view'],item['dimensions'],item['paths'],item['visible_bounds'])
