#!/usr/bin/env python3
"""NAON2 approved-sheet figure isolation: transparent references, not new masters."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/references/naon2-character-sheet-v1.png"
OUT = ROOT / "assets/derivatives/reference-isolates-v03"
VIEWS = {
    "front": (19, 475, 233, 688),
    "three-quarter": (219, 473, 404, 689),
    "back": (388, 474, 601, 689),
}

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf" if bold
        else "/usr/share/fonts/truetype/nanum/NanumSquareRoundR.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for item in candidates:
        if Path(item).is_file():
            return ImageFont.truetype(item, size)
    return ImageFont.load_default(size)

def isolate(source, rect):
    x0, y0, x1, y1 = rect
    rgb = source[y0:y1, x0:x1].copy()
    h, w = rgb.shape[:2]
    assert 100 < h < 300 and 100 < w < 300
    mask = np.full((h,w), cv2.GC_PR_FGD, dtype=np.uint8)
    b=7
    mask[:b,:]=0
    mask[-b:,:]=0
    mask[:,:b]=0
    mask[:,-b:]=0
    rgb16=rgb.astype(np.uint16)
    dark=(np.min(rgb16,axis=2)<145)
    safe=np.zeros((h,w),bool)
    safe[16:-16,16:-16]=True
    mask[dark & safe]=cv2.GC_FGD
    bright=(np.min(rgb16,axis=2)>245)&(np.max(rgb16,axis=2)-np.min(rgb16,axis=2)<9)
    mask[bright & ~dark]=cv2.GC_PR_BGD
    mask[:b,:]=0
    mask[-b:,:]=0
    mask[:,:b]=0
    mask[:,-b:]=0
    bg=np.zeros((1,65),np.float64)
    fg=np.zeros((1,65),np.float64)
    cv2.grabCut(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),mask,None,bg,fg,8,cv2.GC_INIT_WITH_MASK)
    raw=np.where((mask==cv2.GC_BGD)|(mask==cv2.GC_PR_BGD),0,255).astype(np.uint8)
    count,components,stats,_=cv2.connectedComponentsWithStats(raw,8)
    objects=[i for i in range(1,count) if stats[i,cv2.CC_STAT_AREA]>70]
    assert len(objects)==1, ("wrong object count",len(objects))
    shape=(components==objects[0]).astype(np.uint8)*255
    shape=cv2.morphologyEx(shape,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
    contours,_=cv2.findContours(shape,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    filled=np.zeros_like(shape)
    cv2.drawContours(filled,contours,-1,255,cv2.FILLED)
    alpha=cv2.GaussianBlur(filled,(3,3),0.55)
    assert 20000 < np.count_nonzero(alpha) < 40000
    assert not alpha[0,:].any() and not alpha[-1,:].any()
    assert not alpha[:,0].any() and not alpha[:,-1].any()
    return Image.fromarray(np.dstack([rgb,alpha]),"RGBA")

def make_preview(images, destination):
    image=Image.new("RGB",(2400,1120),(250,247,254))
    d=ImageDraw.Draw(image)
    for y in range(1120):
        k=y/1120
        d.line((0,y,2400,y),fill=(int(250-7*k),int(247-8*k),int(254-5*k)))
    d.text((94,50),"NAON2  |  나온이",font=font(72,True),fill=(68,45,112))
    d.text((100,145),"승인 표준 시트에서 직접 분리한 투명 배경 레퍼런스  /  v0.3",font=font(29),fill=(106,91,134))
    for i,(key,label) in enumerate([
        ("front","정면 · FRONT"),
        ("three-quarter","준측면 · 3/4 VIEW"),
        ("back","후면 · BACK"),
    ]):
        left=94+i*740
        d.rounded_rectangle((left,225,left+690,935),radius=42,fill=(255,255,255),outline=(229,219,244),width=4)
        d.text((left+44,260),label,font=font(42,True),fill=(82,59,134))
        src=images[key]
        ratio=min(580/src.width,560/src.height)
        new_size=tuple(round(v*ratio) for v in src.size)
        enlarged=src.resize(new_size,Image.Resampling.LANCZOS)
        image.paste(enlarged,(left+(690-enlarged.width)//2,340+(545-enlarged.height)//2),enlarged)
        d.text((left+52,878),f"원본 크기: {src.width} × {src.height} px",font=font(26),fill=(127,119,144))
    d.line((92,981,2306,981),fill=(214,205,232),width=3)
    d.text((94,1011),"원본 기반 분리본 / 확대 미리보기는 네이티브 고해상도 원화가 아닙니다.",font=font(29),fill=(98,86,123))
    image.save(destination,optimize=True)

def main():
    manifest=json.loads((ROOT/"asset-manifest.json").read_text(encoding="utf-8"))
    entry=next(e for e in manifest["assets"] if e["path"]=="assets/references/naon2-character-sheet-v1.png")
    source_data=SOURCE.read_bytes()
    assert hashlib.sha256(source_data).hexdigest()==entry["sha256"]
    assert len(source_data)==entry["bytes"]
    rgb=np.asarray(Image.open(SOURCE).convert("RGB"))
    assert (rgb.shape[1],rgb.shape[0])==(1536,1024)
    OUT.mkdir(parents=True,exist_ok=True)
    images={}
    report=[]
    for name,rect in VIEWS.items():
        img=isolate(rgb,rect)
        out=OUT/f"naon2-{name}-reference-v03.png"
        img.save(out,optimize=True)
        payload=out.read_bytes()
        images[name]=img
        report.append({"view":name,"filename":out.name,"dimensions":list(img.size),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"source_crop":list(rect),"kind":"approved-source transparent reference (not native high-resolution master)"})
    make_preview(images,OUT/"naon2-three-view-preview-v03.png")
    (OUT/"reference-v03-manifest.json").write_text(json.dumps({"source_file":str(SOURCE.relative_to(ROOT)),"source_sha256":entry["sha256"],"views":report,"status":"segmented reference only; new master pending"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for item in report:
        print(item["view"],item["dimensions"],item["bytes"],item["sha256"])

if __name__=="__main__":
    main()
