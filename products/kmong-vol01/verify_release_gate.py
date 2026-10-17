#!/usr/bin/env python3
"""Read-only NAON2 buyer ZIP technical validator for pre/post-winter releases.

Never equates technical PASS with visual, license, user approval, or Kmong review.

    python verify_release_gate.py FULL_RC.zip WALL_RC.zip
    python verify_release_gate.py FULL_WITH_WINTER.zip WALL_WITH_WINTER.zip \
      --with-winter --winter-master ART_MASTER.png
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
from zipfile import ZipFile, BadZipFile
from PIL import Image

PROFILE = 'NAON2_PROFILE_GUIDE.png'
PROFILE_SHA = '7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac'
WINTER_MASTER = '01_ORIGINAL_ARTWORKS/NAON2_WINTER_INDEPENDENT_ORIGINAL.png'
WINTER_DERIVATIVES = [
    '02_PC_16x9/09_WINTER.png', '03_PC_21x9/09_WINTER.png',
    '04_MOBILE_9x16/09_WINTER.png'
]
WINTER_LOCK = '05_LOCKSCREEN_BONUS/09_WINTER_LOCK.png'
FOLDERS = {
    '02_PC_16x9/': (2560, 1440),
    '03_PC_21x9/': (3440, 1440),
    '04_MOBILE_9x16/': (1440, 2560),
    '05_LOCKSCREEN_BONUS/': (1440, 2560)
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verified_png(blob):
    with Image.open(io.BytesIO(blob)) as img:
        if img.format != 'PNG':
            raise ValueError('Not PNG')
        dims = img.size
        img.verify()
    return dims

def check_zip(path, menu, with_winter, winter_sha):
    full = menu == 'full'
    base_count = 8 if full else 6
    n = base_count + int(with_winter)
    expected = (51 if full else 23) if with_winter else (46 if full else 19)
    needed = {
        '01_ORIGINAL_ARTWORKS/': (13 if full else 0) + int(with_winter),
        '02_PC_16x9/': n,
        '03_PC_21x9/': n,
        '04_MOBILE_9x16/': n,
        '05_LOCKSCREEN_BONUS/': n if full else 0,
    }
    report = {'menu':menu,'path':str(path),'errors':[],'warnings':[]}
    errors = report['errors']
    if not path.is_file():
        errors.append('ZIP does not exist')
        report['technical_pass'] = False
        return report
    report['bytes'] = path.stat().st_size
    if report['bytes'] > 200_000_000:
        errors.append('ZIP exceeds 200MB service limit')
    with path.open('rb') as fp:
        report['sha256'] = hashlib.file_digest(fp, 'sha256').hexdigest()
    try:
        with ZipFile(path) as z:
            paths = z.namelist()
            if len(paths) != len(set(paths)):
                errors.append('Duplicate ZIP filenames')
            if any(p.startswith('/') or '\\' in p or '..' in p.split('/') for p in paths):
                errors.append('Unsafe ZIP filename')
            if z.testzip():
                errors.append('ZIP CRC error')
            pngs = [p for p in paths if p.lower().endswith('.png')]
            report['png_count'] = len(pngs)
            if len(pngs) != expected:
                errors.append(f'Wrong PNG total {len(pngs)}; expected {expected}')
            if PROFILE not in paths:
                errors.append('Profile sheet missing')
            else:
                profile = z.read(PROFILE)
                if sha(profile) != PROFILE_SHA:
                    errors.append('Profile sheet wrong SHA256')
                if verified_png(profile) != (1536,1024):
                    errors.append('Profile sheet wrong dimensions')
            if '00_README_KR.txt' not in paths:
                errors.append('Korean buyer guide missing')
            else:
                guide = z.read('00_README_KR.txt').decode('utf-8')
                if '개인' not in guide:
                    errors.append('Usage rights missing in buyer guide')
                if with_winter and '아직 품질 기준 충족 전' in guide:
                    errors.append('Pending winter message survived final package')
                if not with_winter and '겨울 나온이 독립 원화는 아직' in guide:
                    report['warnings'].append('Winter artwork is not included in RC')
            for folder, required in needed.items():
                assets = [p for p in pngs if p.startswith(folder)]
                if len(assets) != required:
                    errors.append(f'{folder}: {len(assets)} found; expected {required}')
                digests = []
                for member in assets:
                    data = z.read(member)
                    dimensions = verified_png(data)
                    if folder == '01_ORIGINAL_ARTWORKS/':
                        if member == WINTER_MASTER:
                            if min(dimensions) < 1440 or dimensions[0]*dimensions[1] < 2560*1440:
                                errors.append('Winter master source too small')
                        elif dimensions != (1254,1254):
                            errors.append(f'Existing original wrong dimensions: {member}')
                    elif dimensions != FOLDERS[folder]:
                        errors.append(f'{member}: wrong size {dimensions}')
                    digests.append(sha(data))
                if len(set(digests)) != len(digests):
                    errors.append(f'Duplicate byte-identical files in {folder}')
            if with_winter:
                for required in [WINTER_MASTER,*WINTER_DERIVATIVES,*( [WINTER_LOCK] if full else [] )]:
                    if required not in paths:
                        errors.append('Expected winter member missing: '+required)
                if WINTER_MASTER in paths and sha(z.read(WINTER_MASTER)) != winter_sha:
                    errors.append('Winter master differs from approved provided source')
            else:
                if WINTER_MASTER in paths:
                    errors.append('Unapproved winter original found in pre-winter RC')
            report['winter_original_present'] = WINTER_MASTER in paths
    except (BadZipFile, OSError, ValueError, UnicodeError) as exc:
        errors.append('ZIP or media malformed: '+str(exc))
    report['technical_pass'] = not errors
    return report

def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('full',type=Path)
    a.add_argument('wallpaper',type=Path)
    a.add_argument('--with-winter',action='store_true')
    a.add_argument('--winter-master',type=Path)
    a.add_argument('--json',type=Path)
    opt = a.parse_args()
    if opt.with_winter and not opt.winter_master:
        a.error('--with-winter requires --winter-master to compare exact master bytes')
    winter_sha = ''
    if opt.winter_master:
        if not opt.winter_master.is_file():
            a.error('Winter master file not found')
        with opt.winter_master.open('rb') as f:
            winter_sha = hashlib.file_digest(f,'sha256').hexdigest()
    result = [check_zip(opt.full,'full',opt.with_winter,winter_sha),
              check_zip(opt.wallpaper,'wallpaper',opt.with_winter,winter_sha)]
    report = {
        'items':result,
        'technical_pass':all(x['technical_pass'] for x in result),
        'winter_art_in_both':all(x.get('winter_original_present',False) for x in result),
        'winter_master_sha256':winter_sha if opt.with_winter else None,
        'user_art_approval':'UNVERIFIED',
        'kmong_platform_approval':'UNVERIFIED',
        'release_eligible':False,
        'reason':'Technical validation does not prove artwork originality, anatomy, rights, user approval, or platform acceptance.'
    }
    if opt.json:
        opt.json.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['technical_pass'] else 1

if __name__ == '__main__':
    sys.exit(main())
