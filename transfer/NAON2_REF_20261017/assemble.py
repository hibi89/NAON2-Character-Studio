#!/usr/bin/env python3
"""Temporary NAON2 reference archive rebuild from GitHub-hosted binary parts."""
import argparse, hashlib, json, sys, zipfile
from pathlib import Path
here=Path(__file__).resolve().parent
manifest=json.loads((here/"manifest.json").read_text(encoding="utf-8"))
parser=argparse.ArgumentParser()
parser.add_argument("--output",default=str(here/manifest["archive"]))
args=parser.parse_args()
target=Path(args.output)
target.parent.mkdir(parents=True,exist_ok=True)
h=hashlib.sha256()
count=0
with target.open("wb") as fout:
    for p in manifest["parts"]:
        data=(here/p["filename"]).read_bytes()
        if len(data)!=p["bytes"]:
            raise SystemExit(f"size FAIL {p['filename']}: {len(data)} expected {p['bytes']}")
        git_header=b"blob "+str(len(data)).encode("ascii")+bytes([0])
        gitsha=hashlib.sha1(git_header+data).hexdigest()
        if gitsha!=p["git_blob_sha"]:
            raise SystemExit(f"Git blob SHA FAIL {p['filename']}")
        fout.write(data)
        h.update(data)
        count+=len(data)
if count!=manifest["size_bytes"] or h.hexdigest()!=manifest["sha256"]:
    raise SystemExit(f"ZIP SHA/size FAIL {count} {h.hexdigest()}")
with zipfile.ZipFile(target) as z:
    if z.testzip() is not None or len(z.namelist())!=manifest["zip_entries"]:
        raise SystemExit("ZIP CRC/members FAIL")
print(f"PASS {target} size={count} sha256={h.hexdigest()} files={manifest['zip_entries']}")
