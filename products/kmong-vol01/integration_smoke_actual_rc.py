#!/usr/bin/env python3
"""Opt-in local test requiring original ~200MB RCs; never creates approved artwork."""
import argparse, json, tempfile
from pathlib import Path
from PIL import Image,ImageDraw
import winter_release_pipeline as p
import verify_release_gate as g

argparse_parser=argparse.ArgumentParser(description='Quarantined synthetic integration test; original RC ZIP files read-only')
argparse_parser.add_argument('--full',required=True,type=Path)
argparse_parser.add_argument('--wallpaper',required=True,type=Path)
options=argparse_parser.parse_args()
full=options.full
wall=options.wallpaper
print('Validating exact original RC SHA...', flush=True)
p.check_base(full,'full');p.check_base(wall,'wallpaper')
with tempfile.TemporaryDirectory(prefix='naon2_quarantine_test_') as root:
    root=Path(root)
    source=root/'FAKE_ART_NEVER_USE_FOR_SALES.png'
    img=Image.new('RGB',(2560,1440),'#35435d')
    d=ImageDraw.Draw(img)
    d.rectangle((100,100,2450,1320),outline='red',width=25)
    d.text((150,180),'SYNTHETIC TEST DATA / NOT NAON2 ORIGINAL / NOT FOR SALE',fill='white',stroke_width=2,stroke_fill='black')
    img.save(source,'PNG',compress_level=1)
    p.assert_master(source)
    adds=p.make_additions(source)
    for menu,zpath,adds2 in [('full',full,adds),('wallpaper',wall,{k:v for k,v in adds.items() if k in p.TARGETS or k==p.ORIGINAL_KEY})]:
        dest=root/(menu+'.zip')
        info=p.write_package(zpath,dest,adds2,menu=='full')
        rep=g.check_zip(dest,menu,True,p.sha256_file(source))
        assert rep['technical_pass'],rep
        assert rep['winter_original_present'] and rep['png_count']==(51 if menu=='full' else 23)
        print('INTEGRATION_PASS',menu,info['png_count'],info['bytes'],rep['errors'], flush=True)
    with p.ZipFile(full) as z: profile=z.read('NAON2_PROFILE_GUIDE.png')
    pp=p.seller_pages(full,profile,source,root/'pages_full',True)
    pw=p.seller_pages(wall,profile,source,root/'pages_wall',False)
    assert len(pp)==len(pw)==5
    print('LISTING_PASS',len(pp)+len(pw),'images',flush=True)
print('Synthetic inputs and packages auto-deleted; originals unchanged.',flush=True)
