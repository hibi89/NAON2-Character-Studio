#!/usr/bin/env python3
"""Non-destructive NAON2 Vol01 packaging. Does not edit any of the 15 source PNGs."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import hashlib, json, zipfile, os

src=Path("assets/selected/vol01")
out=Path("build/NAON2_WORLD_VOL01_REVIEW")
imgs=out/"marketplace_images"
imgs.mkdir(parents=True,exist_ok=True)
expected={
"ChatGPT 이미지 2026년 10월 17일 오후 01_15_44.png":"ea83deae45d04fb2b337e4fbf2b8a8660e5fae55",
"ChatGPT 이미지 2026년 10월 17일 오후 01_49_17.png":"0b71fe512b92b36d8e5c5f2e661533186a4a7c7e",
"ChatGPT 이미지 2026년 10월 17일 오후 01_49_28.png":"0aa359e4afecae98c3e53d5a904b3d242e5f93c2",
"ChatGPT 이미지 2026년 10월 17일 오후 01_49_52.png":"c99e560645ed7be480a549e3ffed4e743f4c8972",
"ChatGPT 이미지 2026년 10월 17일 오후 01_50_04.png":"bf54ef37cd0214d01fe28ab8dee28a6bd3e02348",
"ChatGPT 이미지 2026년 10월 17일 오후 01_50_13.png":"0cb33185c384448c168f38ea08548e10b4d80f20",
"ChatGPT 이미지 2026년 10월 17일 오후 01_50_28.png":"ff8f7b65f6e8b6c4e7994d21354479c3ed029428",
"ChatGPT 이미지 2026년 10월 17일 오후 01_50_39.png":"e0d55879bb791284946bbcbd9cb5eb7cbb800093",
"ChatGPT 이미지 2026년 10월 17일 오후 01_51_10.png":"1f966b58374f3093be7031d0e83fd3053dbcbd1a",
"ChatGPT 이미지 2026년 10월 17일 오후 01_51_13.png":"071d5ea1573ec782e75b794934e8de05e7405c10",
"ChatGPT 이미지 2026년 10월 17일 오후 01_51_17.png":"39b35fcc59fab80c792832eddc74d610d2b52be8",
"image(20260928-233741).png":"5a6bcdc0281aa393d2aa1b30a24852744b879cdc",
"나온이3.PNG":"cd41df0a7d7da643f24faa9e1c41386c906d0550",
"냥이.png":"745437e1f0dfbce9bba867d64c9b8a8e5ce634ab",
"황금빛 기차 여행의 고양이 친구.png":"691c944694bf6cba6ab38f02aaaee87fda52e639",
}
def sha256(b):return hashlib.sha256(b).hexdigest()
def git_sha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def font(size,bold=False):
    cand=(["/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/nanum/NanumGothic.ttf","/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for p in cand:
        if os.path.isfile(p):return ImageFont.truetype(p,size)
    return ImageFont.load_default()
def tx(d,x,y,s,size=26,color=(248,243,244),bold=False):d.text((x,y),s,font=font(size,bold),fill=color)
def save(im,path,size):
    assert im.size==size
    im.save(path,"JPEG",quality=93,subsampling=0)
    with Image.open(path) as im2:im2.verify()
BG=(21,23,39);TEXT=(250,248,247);SUB=(185,185,207);PURP=(191,161,250)
files=sorted([x for x in src.iterdir() if x.is_file() and x.suffix.lower()==".png"],key=lambda x:x.name)
assert len(files)==15,(len(files),"expected 15 selected PNG")
assert set(x.name for x in files)==set(expected),(set(expected)-set(x.name for x in files))
items=[]
for i,p in enumerate(files,1):
    b=p.read_bytes()
    assert git_sha(b)==expected[p.name],f"Source was modified: {p.name}"
    with Image.open(p) as im:im.verify()
    with Image.open(p) as im:
        im.load()
        art=im.convert("RGB")
        w,h=im.size
    assert w>=100 and h>=100
    items.append((p,art,dict(number=i,filename=p.name,width=w,height=h,size_bytes=len(b),sha256=sha256(b),git_blob_sha=git_sha(b))))
    print(f"PASS {i:02d}/15 {p.name}: {w}x{h} sha256={sha256(b)[:12]}")
# Never re-save original PNG. Only derive separate JPG marketing compositions.
def tile(canvas,x,y,w,h,art,index,pixels):
    dr=ImageDraw.Draw(canvas)
    dr.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=(38,41,61))
    dr.rounded_rectangle((x+14,y+14,x+w-14,y+h-72),radius=12,fill=(23,27,43))
    thumb=ImageOps.contain(art,(w-44,h-108),method=Image.Resampling.LANCZOS)
    canvas.paste(thumb,(x+(w-thumb.width)//2,y+18+((h-104)-thumb.height)//2))
    tx(dr,x+25,y+h-57,f"{index:02d}   {pixels}",25,TEXT,True)
cover=Image.new("RGB",(652,488),BG);d=ImageDraw.Draw(cover)
d.rounded_rectangle((16,17,635,470),radius=22,outline=(117,89,157),width=2)
tx(d,45,45,"NAON2",66,TEXT,True)
tx(d,45,122,"WORLD  /  VOL.01",23,PURP,True)
tx(d,45,160,"나온이의 작은 세계",24,TEXT,True)
tx(d,45,210,"15 ORIGINAL ARTWORKS",20,SUB)
big=sorted(items,key=lambda k:k[2]["width"]*k[2]["height"],reverse=True)
for index,(_,im,_) in enumerate(big[:3]):
    x=47+index*188
    d.rounded_rectangle((x,277,x+174,440),radius=15,fill=(37,42,61))
    thumbnail=ImageOps.contain(im,(160,151))
    cover.paste(thumbnail,(x+(174-thumbnail.width)//2,283+(151-thumbnail.height)//2))
save(cover,imgs/"01_main_652x488.jpg",(652,488))
for group in range(3):
    canv=Image.new("RGB",(1200,1900),BG);d=ImageDraw.Draw(canv)
    tx(d,62,51,"NAON2 WORLD",59,TEXT,True)
    tx(d,64,132,f"ORIGINAL ARTWORKS   /   {group*5+1:02d} — {group*5+5:02d}",27,PURP)
    d.line((64,187,1136,187),fill=(88,76,110),width=2)
    for local,(p,im,m) in enumerate(items[group*5:group*5+5]):
        x=62+(local%2)*552;y=223+(local//2)*529
        tile(canv,x,y,522,504,im,group*5+local+1,f'{m["width"]} × {m["height"]} px')
    tx(d,623,1383,"15 ORIGINALS",41,TEXT,True)
    tx(d,623,1441,"ALL IMAGES INCLUDED",23,PURP,True)
    tx(d,623,1494,"선정 원본 그대로 수록",24,SUB)
    d.line((64,1829,1136,1829),fill=(88,76,110),width=2)
    tx(d,66,1850,"NAON2 WORLD   •   VOL.01   •   ART COLLECTION",21,SUB)
    save(canv,imgs/f'0{group+2}_gallery_{group*5+1:02d}_{group*5+5:02d}_1200x1900.jpg',(1200,1900))
intro=Image.new("RGB",(1200,1800),BG);d=ImageDraw.Draw(intro)
tx(d,73,65,"NAON2",100,TEXT,True)
tx(d,74,185,"어디에든 나오는 호기심 많은 고양이",39,PURP,True)
tx(d,74,250,"나온이의 작은 세계  /  VOL.01",34,TEXT)
d.rounded_rectangle((76,341,1124,1270),radius=25,fill=(39,43,62))
art=big[0][1]
v=ImageOps.contain(art,(1000,890))
intro.paste(v,((1200-v.width)//2,354+(890-v.height)//2))
tx(d,80,1357,"크고 동그란 갈색 눈, 복슬한 꼬리",41,TEXT,True)
tx(d,80,1432,"게임 · 우주 · 기차 · 여행 · 쉼표 같은 순간들",31,SUB)
tx(d,80,1520,"NAON2 ORIGINAL 15 ARTWORKS",33,PURP,True)
tx(d,80,1590,"사용자가 직접 고른 열다섯 장면",32,TEXT)
tx(d,80,1731,"NAON2 WORLD  /  DIGITAL ART COLLECTION",23,SUB)
save(intro,imgs/"05_about_NAON2_1200x1800.jpg",(1200,1800))
spec=Image.new("RGB",(1200,1690),BG);d=ImageDraw.Draw(spec)
tx(d,63,55,"구매자 제공 구성",63,TEXT,True)
tx(d,65,154,"선정 원본 PNG 15장  +  한국어 사용 안내",31,PURP,True)
d.line((65,216,1133,216),fill=(88,76,110),width=2)
for i,(p,art,m) in enumerate(items):
    x=66+(i//8)*557;y=248+(i%8)*170
    d.rounded_rectangle((x,y,x+524,y+150),radius=16,fill=(37,43,63))
    v=ImageOps.contain(art,(126,126))
    spec.paste(v,(x+13+(126-v.width)//2,y+11+(126-v.height)//2))
    tx(d,x+153,y+22,f"ART {i+1:02d}",30,TEXT,True)
    tx(d,x+153,y+65,f'{m["width"]} × {m["height"]} px',26,PURP)
    tx(d,x+153,y+110,"원본 PNG",22,SUB)
tx(d,68,1630,"일부 이미지는 소형 원본입니다. 전체가 2K 배경화면은 아닙니다.",22,SUB)
save(spec,imgs/"06_file_specs_1200x1690.jpg",(1200,1690))
lines="\n".join(f'{i+1:02d}. {m["filename"]}  {m["width"]}x{m["height"]}px' for i,(_,_,m) in enumerate(items))
buyer_text="""NAON2 WORLD Vol.01 — 나온이의 작은 세계

구성: 선정된 원본 PNG 15장, 이 한국어 안내 1개.
디지털 파일만 제공하며 실물 배송은 없습니다.
NAON2는 호기심 많은 고양이 캐릭터입니다.
크고 둥근 갈색 눈, 회갈색과 흰색 털, 분홍빛 귀와 코,
풍성하게 말린 꼬리가 특징입니다.

사용 방법: ZIP을 해제한 뒤 PNG를 열거나 개인 기기의
배경화면으로 설정해 보세요.
일부 원본은 소형 또는 정사각형 이미지이므로
모든 그림이 고해상도 PC/모바일 배경화면에 적합하지는 않습니다.

권리 안내 (정식 판매 전 확인해야 할 조건):
개인 감상 및 개인 기기의 배경화면 사용에 한합니다.
재판매·재배포·상업적 이용 및 굿즈 제작 권한은 포함하지 않습니다.
원본 제작에 생성형 AI 도구를 활용했습니다.
최초 입력 자료의 권리/실제 판매 가능성 검토 및 최종 사용자
승인 후에만 정식 구매자 파일로 활용하세요.

원본 15장 이미지 크기:
"""+lines+"\n"
(out/"USER_GUIDE_KR_DRAFT.txt").write_text(buyer_text,encoding="utf-8")
listing="""나온이 NAON2 일러스트 컬렉션 15종

어디에든 나오는 호기심 많은 고양이, NAON2.
큰 갈색 눈, 회갈색과 하얀 털, 분홍빛 귀와 코, 복슬하게 말린 꼬리.
게임을 하다가 우주로 여행하고, 기차를 타고 새로운 세계를 만나기도 합니다.

이번 Vol.01은 선정된 실제 원본 PNG 작품 15장 전체와
한국어 사용 안내문을 ZIP으로 제공하는 디지털 아트 컬렉션입니다.
각 원본의 픽셀 해상도는 상세 이미지 및 파일 설명에 명시했습니다.
크기가 작은 원본도 포함되므로 모든 원화를 고해상도 벽지로 광고하지 않습니다.

출시 등록 희망가: 5,900원.
향후 7,900원으로 변경할 계획이며 기존 7,900원 판매 이력은 없습니다.
크몽 메인 이미지에는 가격/할인 문구를 넣지 않습니다.
맞춤 제작/다온이는 이 서비스에 포함되지 않습니다.

생성형 AI를 제작 과정에 활용했습니다.
개인 감상/기기 배경화면 사용을 위해 제공하며 재판매·재배포·상업적
이용권은 포함하지 않는 조건으로 검토 중입니다.
폰트 파일을 제공하지 않습니다. 원본 권리 및 판매 카테고리·이용권,
환불 정책 확인 후에만 게시합니다.
"""
(out/"LISTING_COPY_KR_DRAFT.txt").write_text(listing,encoding="utf-8")
meta=[m for _,_,m in items]
(out/"QA_MANIFEST_INTERNAL.json").write_text(json.dumps({"status":"TECHNICAL_CANDIDATE_NOT_APPROVED","count":15,"originals_unchanged":True,"commercial_rights_verified":False,"user_final_approval":False,"images":meta},ensure_ascii=False,indent=2),encoding="utf-8")
buyer=out/"NAON2_WORLD_VOL01_15_ORIGINALS_CANDIDATE.zip"
with zipfile.ZipFile(buyer,"w",compression=zipfile.ZIP_STORED) as z:
    for p,art,m in items:z.write(p,arcname="NAON2_ORIGINAL_15/"+p.name)
    z.write(out/"USER_GUIDE_KR_DRAFT.txt","USER_GUIDE_KR.txt")
with zipfile.ZipFile(buyer) as z:
    assert z.testzip() is None and len(z.namelist())==16
    for p,art,m in items:assert sha256(z.read("NAON2_ORIGINAL_15/"+p.name))==m["sha256"]
assert buyer.stat().st_size<200*1024*1024
summary=f'Originals: 15/15 verified, unmodified\nBuyer ZIP size: {buyer.stat().st_size}\nBuyer ZIP SHA-256: {sha256(buyer.read_bytes())}\nSTATUS: NOT FOR SALE UNTIL RIGHTS + USER APPROVAL\n'
(out/"BUILD_REPORT.txt").write_text(summary,encoding="utf-8")
review=out/"NAON2_WORLD_VOL01_SELLER_REVIEW.zip"
with zipfile.ZipFile(review,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    z.write(buyer,buyer.name,compress_type=zipfile.ZIP_STORED)
    for p in sorted(imgs.glob("*.jpg")):z.write(p,arcname="marketplace_images/"+p.name)
    for name in ["LISTING_COPY_KR_DRAFT.txt","QA_MANIFEST_INTERNAL.json","BUILD_REPORT.txt"]:
        z.write(out/name,arcname="internal_seller_review/"+name)
with zipfile.ZipFile(review) as z:assert z.testzip() is None
print(summary)
print(f'Seller pack: {review.stat().st_size} bytes; sha256 {sha256(review.read_bytes())}')
