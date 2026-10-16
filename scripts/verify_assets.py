"""Validate NAON2 source/reference image integrity; no external dependencies."""
from pathlib import Path
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "asset-manifest.json").read_text(encoding="utf-8"))
failures = 0
for entry in manifest["assets"]:
    path = ROOT / entry["path"]
    if not path.is_file():
        print(f"FAIL MISSING: {entry['path']}")
        failures += 1
        continue
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    is_png = data[:8] == b"\x89PNG\r\n\x1a\n"
    dimensions = list(struct.unpack(">II", data[16:24])) if is_png and len(data) >= 24 else None
    valid = digest == entry["sha256"] and len(data) == entry["bytes"] and dimensions == entry["pixels"]
    print(f"{'PASS' if valid else 'FAIL'}: {entry['path']} ({dimensions}, {len(data)} bytes)")
    if not valid:
        failures += 1
sys.exit(1 if failures else 0)
