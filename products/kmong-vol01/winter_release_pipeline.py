#!/usr/bin/env python3
"""NAON2 winter artwork integration — gated by manually confirmed artwork.

No image generation, original source modification, platform upload, or approval fabrication.
Requires Pillow, Python 3.11+.

Usage:
    python winter_release_pipeline.py inspect --master winter-original.png --out inspection/
    python winter_release_pipeline.py package --master winter-original.png \
      --approval user-signed-review.json --full full-RC.zip --wallpaper wallpaper-RC.zip --out build/

'Package' produces REVIEW_CANDIDATE ZIPs, never uploads/submits to Kmong.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

PROFILE_SHA = "7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac"
BASE_SHA = {
    "full": "2acd5725434dde4dbd80d35ec7f6fa132eec20da4685425437dc8a6cb24f470a",
    "wallpaper": "f435e6729c5892afcf332cbe879e8ca51de2b00c9f0bb63013b9fe6cfad4ad14",
}
WINTER_KEY = "09_WINTER"
ORIGINAL_KEY = "01_ORIGINAL_ARTWORKS/NAON2_WINTER_INDEPENDENT_ORIGINAL.png"
TARGETS = {
    "02_PC_16x9/09_WINTER.png": (2560, 1440),
    "03_PC_21x9/09_WINTER.png": (3440, 1440),
    "04_MOBILE_9x16/09_WINTER.png": (1440, 2560),
}
LOCK_KEY = "05_LOCKSCREEN_BONUS/09_WINTER_LOCK.png"
PRODUCTION_APPROVAL_KEYS = (
    "is_independent_new_artwork", "not_screenshot_or_crop", "not_upsampled_source",
    "character_identity_approved", "exactly_four_legs_visual_qa", "eyes_teeth_tail_visual_qa",
    "image_quality_approved", "usage_rights_verified", "user_approved_for_packaging",
)


def sha256_file(p: Path):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def assert_master(master: Path):
    if not master.is_file():
        raise ValueError('Winter original image missing')
    with Image.open(master) as im:
        im.verify()
    with Image.open(master) as im:
        if im.format != "PNG":
            raise ValueError('Winter must be a PNG original')
        w, h = im.size
        if min(w, h) < 1440 or w * h < 2560 * 1440:
            raise ValueError(f'Master {w}x{h} below native 2560x1440-equivalent resolution; do not upscale to bypass')
        if im.mode in ('RGBA', 'LA') or 'transparency' in im.info:
            a = im.convert('RGBA').getchannel('A')
            lo, hi = a.getextrema()
            if lo < 255:
                raise ValueError('Master has transparency: a complete standalone scene is required')
        return {"master":master.name, "dimensions":[w,h], "sha256":sha256_file(master),
                "bytes":master.stat().st_size, "format":"PNG"}


def check_approval(meta: dict, master_hash: str):
    issues=[]
    if meta.get('winter_master_sha256') != master_hash:
        issues.append('Winter master SHA mismatch')
    if meta.get('profile_sheet_sha256') != PROFILE_SHA:
        issues.append('Wrong profile master reference')
    if meta.get('reviewed_by') != 'user':
        issues.append('User final review not attested')
    for k in PRODUCTION_APPROVAL_KEYS:
        if meta.get(k) is not True:
            issues.append('Missing confirmed manual review: '+k)
    if not meta.get('rights_basis') or not meta.get('source_provenance'):
        issues.append('Rights basis/source provenance not documented')
    if issues:
        raise ValueError('Release gate BLOCKED:\n - '+'\n - '.join(issues))


def render(master: Image.Image, size, lock=False):
    """Unstretched square art on a dim blurred extension (derivative, not native new art)."""
    source=master.convert('RGB'); W,H=size
    r=max(W/source.width,H/source.height)
    expanded=source.resize((round(source.width*r),round(source.height*r)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(W,H))
    canvas.paste(expanded,((W-expanded.width)//2,(H-expanded.height)//2))
    canvas=canvas.filter(ImageFilter.GaussianBlur(max(20,int(min(W,H)*.035))))
    canvas=ImageEnhance.Brightness(canvas).enhance(0.64)
    side=min(int(H*.93), int(W*.93)) if W>H else min(int(W*.96),int(H*.59))
    side=max(2,side)
    top=(H-side)//2 if W>H else int(H*.38-side*.5)
    top=max(0,min(H-side,top))
    subject=source.resize((side,side),Image.Resampling.LANCZOS) if source.width==source.height else fit_inside(source,side)
    # Non-square originals remain entirely visible, never anamorphically stretched.
    if subject.size!=(side,side):
        subject=letterbox(subject,side)
    mask=Image.new('L',(side,side));d=ImageDraw.Draw(mask)
    margin=max(12,round(side*.04))
    d.rounded_rectangle((margin,margin,side-margin,side-margin),radius=round(side*.07),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(max(6,round(side*.035))))
    canvas.paste(subject,((W-side)//2,top),mask)
    if lock:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(overlay)
        for y in range(0,round(H*.28),3):
            alpha=round(130*max(0,1-y/(H*.28)))
            d.rectangle((0,y,W,y+3),fill=(0,0,15,alpha))
        canvas=Image.alpha_composite(canvas.convert('RGBA'),overlay).convert('RGB')
    return canvas


def fit_inside(src,dim):
    img=src.copy();img.thumbnail((dim,dim),Image.Resampling.LANCZOS);return img


def letterbox(src,dim):
    result=Image.new('RGB',(dim,dim),src.getpixel((src.width//2,src.height//2)))
    result.paste(src,((dim-src.width)//2,(dim-src.height)//2));return result


def png_bytes(img):
    buf=io.BytesIO();img.save(buf,format='PNG',compress_level=3);return buf.getvalue()


def safe_members(z: ZipFile):
    members=z.namelist()
    if len(members)!=len(set(members)):
        raise ValueError('Duplicate ZIP paths')
    if any(n.startswith('/') or '..' in n.split('/') or '\\' in n for n in members):
        raise ValueError('Unsafe ZIP path')
    bad=z.testzip()
    if bad:raise ValueError('ZIP CRC failed at '+bad)
    return members


def check_base(path:Path,menu:str):
    if not path.exists():raise ValueError(f'Missing {menu} RC ZIP')
    digest=sha256_file(path)
    if digest!=BASE_SHA[menu]:
        raise ValueError(f'{menu} ZIP changed; expected pinned {BASE_SHA[menu]}, got {digest}')
    with ZipFile(path) as z:
        members=safe_members(z)
        if sha256_bytes(z.read('NAON2_PROFILE_GUIDE.png'))!=PROFILE_SHA:
            raise ValueError('Original buyer ZIP has wrong common profile sheet')
        if any('WINTER' in name.upper() for name in members):
            raise ValueError('Base already contains winter assets; refuse duplicate insertion')
        count=len([x for x in members if x.lower().endswith('.png')])
        if count!=(46 if menu=='full' else 19):
            raise ValueError('Base PNG count changed unexpectedly')
    return digest


def update_readme(old:bytes, full:bool):
    original=old.decode('utf-8')
    pending='이번 기획의 겨울 나온이 독립 원화는 아직 품질 기준 충족 전이므로 이 RC 패키지에 포함하지 않았습니다.'
    if pending not in original:
        raise ValueError('Readme template unexpectedly changed')
    detail=('겨울 독립 원화 PNG 1장 + PC 16:9/21:9, 모바일 9:16, 잠금화면 각 1장' if full
            else '겨울 독립 원화 PNG 1장 + PC 16:9/21:9, 모바일 9:16 파생본 각 1장')
    return original.replace(pending,detail+'\n원화와 화면비별 배경화면을 구분하며 2560/3440/1440px 파생 캔버스는 별도 네이티브 원화가 아닙니다.').replace('시안 검수용 RC','사용자 승인 후 최종 확인용').encode('utf-8')


def write_package(old_zip:Path, dst:Path, additions:dict, full:bool):
    if dst.exists():raise ValueError(f'Refusing to overwrite {dst}')
    temp=dst.with_suffix('.tmp')
    if temp.exists():raise ValueError(f'Temporary output exists: {temp}')
    try:
        with ZipFile(old_zip) as original, ZipFile(temp,'w',ZIP_DEFLATED,compresslevel=2,allowZip64=True) as output:
            safe_members(original)
            for member in original.infolist():
                if member.filename=='00_README_KR.txt':
                    value=update_readme(original.read(member),full)
                else:
                    value=original.read(member)
                output.writestr(member.filename,value)
            for name,data in sorted(additions.items()):
                output.writestr(name,data)
        with ZipFile(temp) as built:
            n=safe_members(built)
            pngs=[x for x in n if x.lower().endswith('.png')]
            if len(pngs)!=(51 if full else 23):
                raise ValueError('Final PNG count mismatch')
            if sha256_bytes(built.read('NAON2_PROFILE_GUIDE.png'))!=PROFILE_SHA:
                raise ValueError('Profile changed in packaging')
            for k in additions:
                with Image.open(io.BytesIO(built.read(k))) as im:
                    im.verify()
        if temp.stat().st_size > 200_000_000:
            raise ValueError("Kmong 200MB per ZIP cap exceeded")
        os.replace(temp,dst)
        return {'file':dst.name,'sha256':sha256_file(dst),'bytes':dst.stat().st_size,
                'png_count':len(pngs),'crc':'PASS'}
    finally:
        if temp.exists():temp.unlink()


def make_additions(master:Path):
    with Image.open(master) as im:
        art=im.convert('RGB')
        assets={k:png_bytes(render(art,size)) for k,size in TARGETS.items()}
        assets[LOCK_KEY]=png_bytes(render(art,(1440,2560),True))
        assets[ORIGINAL_KEY]=master.read_bytes()
        return assets


def make_preview(master:Path,out:Path):
    out.mkdir(parents=True,exist_ok=True)
    with Image.open(master) as im:
        im=im.convert('RGB')
        # Render only the winter artwork without other product-panel marketing text.
        thumb=im.copy();thumb.thumbnail((950,950),Image.Resampling.LANCZOS)
        thumb.save(out/'WINTER_ART_CONTACT_PREVIEW_NOT_FINAL.jpg',quality=91)
        pc=render(im,(1280,720));pc.save(out/'WINTER_PC_LAYOUT_PREVIEW.jpg',quality=90)
        phone=render(im,(540,960));phone.save(out/'WINTER_MOBILE_LAYOUT_PREVIEW.jpg',quality=89)


def font_obj(size):
    options=["/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf",
             "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
             "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf"]
    for f in options:
        if Path(f).exists():return ImageFont.truetype(f,size)
    raise ValueError("Korean-capable listing font unavailable; do not ship broken Hangul text")


def seller_pages(original_zip: Path, profile: bytes, winter_master: Path,
                 folder: Path, is_full: bool):
    """New, accurate post-winter listing JPGs. Listing binary is NOT a customer deliverable."""
    folder.mkdir(parents=True,exist_ok=False)
    def put(draw,xy,s,sz,col='#f3f5ff'):
        draw.text(xy,s,fill=col,font=font_obj(sz))
    with Image.open(io.BytesIO(profile)) as base:
        im=base.convert('RGB')
        # Main: profile sheet unmodified, just scaled to fit and given neutral side margins.
        img=Image.new('RGB',(652,488),'#fff5f1');cp=im.copy();cp.thumbnail((646,484),Image.Resampling.LANCZOS)
        img.paste(cp,((652-cp.width)//2,(488-cp.height)//2))
        img.save(folder/'01_MAIN_652x488.jpg',quality=95)
        p=Image.new('RGB',(1200,1360),'#101a31');d=ImageDraw.Draw(p)
        put(d,(56,48),'NAON2 나온이 프로필 시트',49)
        put(d,(56,120),'모든 상품 공통 증정 · 1536×1024 PNG',30,'#b0c2f0')
        cp=im.copy();cp.thumbnail((1100,735),Image.Resampling.LANCZOS)
        p.paste(cp,((1200-cp.width)//2,196))
        put(d,(55,1020),'회갈색 · 흰색 털 · 복슬한 꼬리',32)
        put(d,(55,1110),'원본 프로필 PNG를 두 메뉴 모두에 포함',28,'#d0dafa')
        p.save(folder/'02_PROFILE_1200x1360.jpg',quality=92)

    with ZipFile(original_zip) as z:
        source=sorted(n for n in z.namelist() if n.startswith('02_PC_16x9/') and n.endswith('.png'))
        source=source[:8] if is_full else source[:6]
        samples=[(f'기존 테마 {i+1}', z.read(n)) for i,n in enumerate(source)]
    samples.append(('신규 겨울',winter_master.read_bytes()))
    page=Image.new('RGB',(1200,1990),'#11182e');d=ImageDraw.Draw(page)
    put(d,(52,42),'NAON2 테마 미리보기',49)
    put(d,(52,120),'신규 겨울 독립 원화 포함 · 사용자 승인 후 등록',26,'#a8bef0')
    for i,(label,blob) in enumerate(samples):
        x=49+(i%3)*386;y=214+(i//3)*575
        with Image.open(io.BytesIO(blob)) as preview:
            thumb=preview.convert('RGB');thumb.thumbnail((357,460),Image.Resampling.LANCZOS)
        tile=Image.new('RGB',(355,480),'#28314c')
        tile.paste(thumb,((355-thumb.width)//2,(480-thumb.height)//2))
        page.paste(tile,(x,y))
        put(d,(x+8,y+490),label,25)
    page.save(folder/'03_THEME_GALLERY_1200x1990.jpg',quality=90)

    page=Image.new('RGB',(1200,1580),'#111b31');d=ImageDraw.Draw(page)
    put(d,(55,50),'NAON2 구성 · 해상도 안내',47)
    if is_full:
        rows=[('메뉴','디지털 컬렉션 19,900원'),('독립 원화','14장 · 원본 13 + 신규 겨울 1'),
              ('PC 16:9 / 21:9','각 9장 · 2560×1440 / 3440×1440'),
              ('모바일 9:16','9장 · 1440×2560'),('잠금화면','9장 · 1440×2560'),
              ('공통 프로필','1장 · 1536×1024'),('합계','PNG 51장')]
    else:
        rows=[('메뉴','배경화면 팩 9,900원'),('테마','7개 · 기존 6 + 겨울 1'),('겨울 신규 원화','1장 · 고화질 독립 PNG'),
              ('PC 16:9','7장 · 2560×1440'),('PC 21:9','7장 · 3440×1440'),
              ('모바일 9:16','7장 · 1440×2560'),('공통 프로필','1장 · 1536×1024'),
              ('합계','PNG 23장')]
    for i,(a,b) in enumerate(rows):
        y=170+i*(136 if not is_full else 152)
        d.rounded_rectangle((50,y,1150,y+123),radius=22,fill='#263452')
        put(d,(77,y+26),a,30)
        put(d,(410,y+27),b,27,'#cbdafc')
    for i,line in enumerate(['PC·모바일 파일은 원화의 화면비 맞춤 파생 이미지입니다.',
                             '원화 1254px를 2K/4K 네이티브 그림으로 표기하지 않습니다.',
                             'AI 활용 제작 · 개인 비상업적 사용 · 재배포/재판매 금지']):
        put(d,(59,1300+i*70),line,23,'#d1def7')
    page.save(folder/'04_DELIVERY_DETAILS_1200x1580.jpg',quality=92)

    with Image.open(winter_master) as winter:
        p=Image.new('RGB',(1200,1500),'#121b30');d=ImageDraw.Draw(p)
        put(d,(55,48),'WINTER · 겨울 나온이',53)
        put(d,(55,124),'신규 독립 원화 · 양쪽 메뉴에 포함',29,'#cdd8fe')
        w=winter.convert('RGB');w.thumbnail((1100,1100),Image.Resampling.LANCZOS)
        p.paste(w,((1200-w.width)//2,220))
        p.save(folder/'05_WINTER_1200x1500.jpg',quality=93)
    for file,expected in [('01_MAIN_652x488.jpg',(652,488)),('02_PROFILE_1200x1360.jpg',(1200,1360)),
                          ('03_THEME_GALLERY_1200x1990.jpg',(1200,1990)),
                          ('04_DELIVERY_DETAILS_1200x1580.jpg',(1200,1580)),
                          ('05_WINTER_1200x1500.jpg',(1200,1500))]:
        with Image.open(folder/file) as im:
            if im.size!=expected:raise ValueError('Seller page invalid dimensions: '+file)
            im.verify()
    return [x.name for x in sorted(folder.glob('*.jpg'))]


def cmd_inspect(a):
    meta=assert_master(a.master)
    make_preview(a.master,a.out)
    meta['status']='INSPECT_ONLY_NOT_FOR_SALE'
    meta['unverified']=['four legs','eyes/teeth/tail','independent artwork provenance','rights','user approval']
    (a.out/'WINTER_INSPECTION.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps(meta,ensure_ascii=False,indent=2))


def cmd_package(a):
    art=assert_master(a.master)
    approval=json.loads(a.approval.read_text('utf-8'))
    check_approval(approval,art['sha256'])
    check_base(a.full,'full');check_base(a.wallpaper,'wallpaper')
    a.out.mkdir(parents=True,exist_ok=True)
    additions=make_additions(a.master)
    final_full=dict(additions)
    final_wall={k:v for k,v in additions.items() if k in TARGETS or k==ORIGINAL_KEY}
    z1=a.out/'NAON2_FULL_COLLECTION_19900_WITH_WINTER_USER_REVIEW.zip'
    z2=a.out/'NAON2_WALLPAPER_PACK_9900_WITH_WINTER_USER_REVIEW.zip'
    with tempfile.TemporaryDirectory(prefix='naon2_winter_',dir=a.out) as scratch:
        stage=Path(scratch)
        stage_full=stage/z1.name;stage_wall=stage/z2.name
        r1=write_package(a.full,stage_full,final_full,True)
        r2=write_package(a.wallpaper,stage_wall,final_wall,False)
        with ZipFile(a.full) as base:
            profile=base.read('NAON2_PROFILE_GUIDE.png')
        jpgs={}
        jpgs['full']=seller_pages(a.full,profile,a.master,stage/'LISTING_FULL',True)
        jpgs['wallpaper']=seller_pages(a.wallpaper,profile,a.master,stage/'LISTING_WALLPAPER',False)
        report={'status':'USER_FINAL_RELEASE_REVIEW_REQUIRED','winter_master':art,'base_originals_untouched':True,
                'packages':[r1,r2], 'listing_pages':jpgs,
                'post_build_requirements':['visually inspect new art and every derived crop',
                 'user approves buyer ZIPs and final listing JPGs',
                 'Codex checks actual Kmong 840876 options only after user signoff']}
        (stage/'FINAL_REVIEW_QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
        make_preview(a.master,stage/'PREVIEW')
        # Publish together only after both packages + 10 JPGs pass technical QC.
        for item in stage.iterdir():
            target=a.out/item.name
            if target.exists():raise ValueError('Output exists; refusing overwrite: '+str(target))
        for item in stage.iterdir():
            os.replace(item,a.out/item.name)
    print(json.dumps(report,ensure_ascii=False,indent=2))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    i=sub.add_parser('inspect',help='Quality information and art-only previews; no approval needed')
    i.add_argument('--master',type=Path,required=True);i.add_argument('--out',type=Path,required=True)
    q=sub.add_parser('package',help='Requires explicit manual user approval manifest')
    q.add_argument('--master',type=Path,required=True)
    q.add_argument('--approval',type=Path,required=True)
    q.add_argument('--full',type=Path,required=True)
    q.add_argument('--wallpaper',type=Path,required=True)
    q.add_argument('--out',type=Path,required=True)
    try:
        a=p.parse_args(argv)
        (cmd_inspect if a.command=='inspect' else cmd_package)(a)
        return 0
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:
        print('BLOCKED:',e,file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
