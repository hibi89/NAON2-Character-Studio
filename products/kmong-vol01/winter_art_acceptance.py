#!/usr/bin/env python3
"""Winter NAON2 original artwork gate. Read-only, no implied user approval."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image

PROFILE_SHA="7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac"
REQUIRED=[
 "is_independent_new_artwork","not_screenshot_or_crop","not_upsampled_source",
 "character_identity_approved","exactly_four_legs_visual_qa","eyes_teeth_tail_visual_qa",
 "image_quality_approved","usage_rights_verified","user_approved_for_packaging"
]
def digest(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""):h.update(block)
 return h.hexdigest()
def check(master,approval):
 errors=[]
 master=Path(master)
 if not master.is_file():return {"approved":False,"errors":["Winter master file missing"]}
 try:
  with Image.open(master) as im:im.verify()
  with Image.open(master) as im:
   if im.format!="PNG":errors.append("Expected PNG")
   w,h=im.size
   if w<2048 or h<2048:errors.append("Independent master requires actual >=2048x2048 source")
   if im.mode in ("RGBA","LA") and im.convert("RGBA").getchannel("A").getextrema()[0]<255:
    errors.append("Transparent unfinished scene")
 except Exception as ex:
  errors.append("Invalid or truncated image: "+str(ex))
 sha=digest(master)
 if approval is None:
  errors.append("Explicit user review manifest missing")
 else:
  try:
   a=json.loads(Path(approval).read_text("utf-8"))
   if a.get("winter_master_sha256")!=sha:errors.append("Winter master checksum mismatch")
   if a.get("profile_sheet_sha256")!=PROFILE_SHA:errors.append("Wrong character profile sheet")
   if a.get("reviewed_by")!="user":errors.append("Manual user review missing")
   if not a.get("rights_basis") or not a.get("source_provenance"):
    errors.append("Rights/source records missing")
   for key in REQUIRED:
    if a.get(key) is not True:errors.append("Manual quality approval missing: "+key)
  except (OSError,ValueError) as ex:
   errors.append("Approval manifest unreadable: "+str(ex))
 return {"approved":not errors,"master_sha256":sha,"errors":errors,
         "notice":"The checklist is an attestation, not image-recognition proof. Final user approval still required."}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--master",type=Path,required=True)
 p.add_argument("--approval",type=Path)
 p.add_argument("--report",type=Path)
 args=p.parse_args()
 result=check(args.master,args.approval)
 body=json.dumps(result,ensure_ascii=False,indent=2)
 if args.report:args.report.write_text(body,encoding="utf-8")
 print(body)
 return 0 if result["approved"] else 2
if __name__=="__main__":sys.exit(main())
