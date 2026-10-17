#!/usr/bin/env python3
"""NAON2 two-menu read-only ZIP QC. Technical PASS never means release approval.
Run: python verify_release_gate.py FULL.zip WALLPAPER.zip --json result.json
"""
import argparse, hashlib, io, json, struct, sys
from PIL import Image
from pathlib import Path
from zipfile import ZipFile

PROFILE="NAON2_PROFILE_GUIDE.png"
PROFILE_HASH="7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac"
SIZES={
 "01_ORIGINAL_ARTWORKS/":(1254,1254),
 "02_PC_16x9/":(2560,1440),
 "03_PC_21x9/":(3440,1440),
 "04_MOBILE_9x16/":(1440,2560),
 "05_LOCKSCREEN_BONUS/":(1440,2560),
}
def sha(content):
 return hashlib.sha256(content).hexdigest()
def png_size(content):
 if content[:8]!=b'\x89PNG\r\n\x1a\n' or content[12:16]!=b'IHDR':
  raise ValueError("Invalid PNG signature/IHDR")
 return struct.unpack('>II',content[16:24])
def check(path,menu):
 full=menu=="full"
 expected=46 if full else 19
 n=8 if full else 6
 needed={"01_ORIGINAL_ARTWORKS/":13 if full else 0,
         "02_PC_16x9/":n,"03_PC_21x9/":n,"04_MOBILE_9x16/":n,
         "05_LOCKSCREEN_BONUS/":n if full else 0}
 result={"menu":menu,"path":str(path),"errors":[],"warnings":[]}
 err=result["errors"]
 if not path.is_file():
  err.append("ZIP file missing");result["technical_pass"]=False
  return result
 result["bytes"]=path.stat().st_size
 with path.open("rb") as stream:
  result["sha256"]=hashlib.file_digest(stream,"sha256").hexdigest()
 if result["bytes"]>200*1024*1024:
  err.append("Package exceeds 200 MiB")
 with ZipFile(path) as z:
  bad=z.testzip()
  result["crc"]="PASS" if bad is None else "FAIL"
  if bad:err.append("ZIP corrupt member: "+bad)
  members=z.namelist()
  if len(members)!=len(set(members)):err.append("ZIP contains duplicate paths")
  if any(x.startswith("/") or ".." in x.split("/") for x in members):err.append("ZIP contains unsafe paths")
  pngs=[x for x in members if x.lower().endswith(".png")]
  result["png_count"]=len(pngs)
  if len(pngs)!=expected:err.append("Wrong PNG count")
  if PROFILE not in members:err.append("Mandatory profile missing")
  else:
   data=z.read(PROFILE)
   if png_size(data)!=(1536,1024):err.append("Incorrect profile size")
   if sha(data)!=PROFILE_HASH:err.append("Incorrect profile master SHA256")
  if "00_README_KR.txt" not in members:err.append("Korean buyer guide missing")
  else:
   guide=z.read("00_README_KR.txt").decode("utf-8")
   if "개인" not in guide:err.append("Usage rights not explained")
   if "겨울 나온이 독립 원화는 아직" in guide:
    result["warnings"].append("Winter illustration explicitly pending")
  for folder,dim in SIZES.items():
   names=[x for x in pngs if x.startswith(folder)]
   if len(names)!=needed[folder]:
    err.append(f"{folder} count {len(names)} != {needed[folder]}")
   unique=set()
   for name in names:
    blob=z.read(name)
    try:
     if png_size(blob)!=dim:err.append(f"Bad image resolution: {name}")
     with Image.open(io.BytesIO(blob)) as im: im.verify()
    except Exception as e:err.append(f"Broken PNG: {name}: {e}")
    unique.add(sha(blob))
   if len(unique)!=len(names):err.append(f"Duplicate byte-identical images in {folder}")
  result["winter_found"]=any("WINTER" in x.upper() or "겨울" in x for x in pngs)
  if not result["winter_found"]:
   result["warnings"].append("NEW INDEPENDENT WINTER ART MISSING")
 result["technical_pass"]=not err
 return result
def main():
 p=argparse.ArgumentParser()
 p.add_argument("full",type=Path)
 p.add_argument("wallpaper",type=Path)
 p.add_argument("--json",type=Path)
 a=p.parse_args()
 items=[check(a.full,"full"),check(a.wallpaper,"wallpaper")]
 report={
  "items":items,
  "technical_pass":all(x["technical_pass"] for x in items),
  "winter_art_in_both":all(x.get("winter_found",False) for x in items),
  "character_visual_approval":"PENDING",
  "licenses_and_platform":"FINAL_REVIEW_PENDING",
  "release_eligible":False,
  "reason":"Technical validation cannot substitute for winter originality, visual identity, user approval, rights, or Kmong review."
 }
 if a.json:a.json.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report["technical_pass"] else 1
if __name__=="__main__":sys.exit(main())
