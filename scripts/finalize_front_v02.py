#!/usr/bin/env python3
"""Preserve NAON2 front candidate v2 and make a padded 2048px display EXPORT.
Native source is 1254px; the 2048px export is NOT newly drawn native 2K artwork.
No change to the face, hair/fur markings, body pose or tail shape.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"assets/candidates/front-v02/naon2-front-candidate-v02-raw.png"
OUT=SRC.parent/"outputs"
REF=ROOT/"assets/derivatives/reference-isolates-v03/naon2-front-reference-v03.png"
EXPECTED="fcf6cd58be831bc66ebf72039061fa0d545696ac79f0c3396247eca78b48d059"

def main():
    assert hashlib.sha256(SRC.read_bytes()).hexdigest()==EXPECTED, "Source SHA mismatch"
    original=Image.open(SRC).convert("RGBA")
    assert original.size==(1254,1254), "Source dimensions changed"
    pixels=np.array(original)
    edge_report={}
    for name,edge in (("top",pixels[0,:,:]),("bottom",pixels[-1,:,:]),("left",pixels[:,0,:]),("right",pixels[:,-1,:])):
        edge_report[name]={"nonzero_alpha":int(np.count_nonzero(edge[:,3])), "strong_alpha":int(np.count_nonzero(edge[:,3]>12))}
        edge[edge[:,3]<=12,3]=0
        assert not np.any(edge[:,3]>12), "Actual artwork clipped at "+name
    padded=Image.new("RGBA",(1498,1498),(0,0,0,0))
    padded.alpha_composite(Image.fromarray(pixels,mode="RGBA"),(182,122))
    display=padded.resize((2048,2048),Image.Resampling.LANCZOS)
    alpha=np.array(display.getchannel("A"))
    yy,xx=np.where(alpha>12)
    bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    margin=[bbox[0],bbox[1],2048-bbox[2],2048-bbox[3]]
    assert min(margin)>=100, "Unsafe margins"
    assert abs(margin[0]-margin[2])<=5, "Horizontal subject not centered"
    assert not any(np.any(e>12) for e in (alpha[0,:],alpha[-1,:],alpha[:,0],alpha[:,-1]))
    OUT.mkdir(parents=True,exist_ok=True)
    padded.save(OUT/"naon2-front-v02-padded-1498-native-canvas.png",optimize=True)
    display.save(OUT/"naon2-front-v02-2048-upscaled-transparent.png",optimize=True)
    for color,name in (("#FFFFFF","white"),("#151425","dark")):
        bg=Image.new("RGBA",(2048,2048),color)
        bg.alpha_composite(display)
        bg.convert("RGB").save(OUT/f"naon2-front-v02-preview-{name}-2048.jpg",quality=94,subsampling=0,optimize=True)
    images=[]
    if REF.is_file(): images.append(("Approved sheet crop 214px",Image.open(REF).convert("RGBA")))
    images += [("Original candidate v2 1254px",original),("2048px padded display (upscale)",display)]
    board=Image.new("RGB",(2100,800),"#f6f2fc")
    draw=ImageDraw.Draw(board)
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",25)
    except OSError:font=ImageFont.load_default()
    for i,(title,img) in enumerate(images[:3]):
        left=55+i*690
        canvas=Image.new("RGBA",(570,570),"white")
        scale=min(540/img.width,540/img.height)
        thumb=img.resize((round(img.width*scale),round(img.height*scale)),Image.Resampling.LANCZOS)
        canvas.alpha_composite(thumb,((570-thumb.width)//2,(570-thumb.height)//2))
        board.paste(canvas.convert("RGB"),(left,110))
        draw.text((left+8,48),title,fill="#2f214b",font=font)
        draw.text((left+8,698),f"Pixels: {img.width} x {img.height}",fill="#2f214b",font=font)
    board.save(OUT/"naon2-front-v02-comparison.png",optimize=True)
    manifest={"stage":"review-candidate-NOT-official-master","source_sha256":EXPECTED,"source_native_px":[1254,1254],"export_px":[2048,2048],"upscaling":True,"new_native_detail":False,"transparent_padding_px":122,"subject_horizontal_shift_px":60,"subject_bbox_2048":bbox,"subject_margins_2048_left_top_right_bottom":margin,"edge_alpha_counts":edge_report,"signoff":"requires user review and commercial-rights checks"}
    (OUT/"QA-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False))

if __name__=="__main__": main()
