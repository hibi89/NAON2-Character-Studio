#!/usr/bin/env python3
"""Offline safety and integration tests; fixtures are NOT saleable artwork."""
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
import winter_release_pipeline as p


def tiny_png():
    b=io.BytesIO();Image.new('RGB',(12,12),'#552d93').save(b,'PNG');return b.getvalue()


class WinterPipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def make_master(self, wh=(2048,2048), mode='RGB'):
        path=self.root/'TEST_ONLY_NOT_ORIGINAL.png'
        Image.new(mode,wh,'#544178').save(path,'PNG')
        return path

    def test_reject_missing_master(self):
        with self.assertRaisesRegex(ValueError,'missing'):
            p.assert_master(self.root/'none.png')

    def test_reject_small_upscale(self):
        with self.assertRaisesRegex(ValueError,'2560x1440'):
            p.assert_master(self.make_master((1000,1000)))

    def test_reject_transparent_masters(self):
        path=self.make_master(mode='RGBA')
        im=Image.open(path);im.putalpha(150);im.save(path)
        with self.assertRaisesRegex(ValueError,'transparency'):
            p.assert_master(path)

    def test_approve_gate_denies_default_and_mismatch(self):
        master=self.make_master();digest=p.sha256_file(master)
        with self.assertRaisesRegex(ValueError,'Missing confirmed'):
            p.check_approval({'winter_master_sha256':digest,'profile_sheet_sha256':p.PROFILE_SHA,'reviewed_by':'user'},digest)
        meta={k:True for k in p.PRODUCTION_APPROVAL_KEYS}
        meta.update(winter_master_sha256='deadbeef',profile_sheet_sha256=p.PROFILE_SHA,reviewed_by='user',rights_basis='TEST',source_provenance='TEST')
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):
            p.check_approval(meta,digest)

    def test_landscape_native_source_accepted(self):
        master=self.make_master((2560,1440))
        dims=p.assert_master(master)['dimensions']
        self.assertEqual(dims,[2560,1440])

    def test_wallpaper_contains_independent_original_as_well_as_derivatives(self):
        fake_profile=tiny_png()
        initial=p.PROFILE_SHA
        p.PROFILE_SHA=hashlib.sha256(fake_profile).hexdigest()
        self.addCleanup(setattr,p,'PROFILE_SHA',initial)
        src=self.root/'wallpaper_synthetic_input.zip'
        out=self.root/'wallpaper_synthetic_output.zip'
        with ZipFile(src,'w',ZIP_DEFLATED) as z:
            z.writestr('NAON2_PROFILE_GUIDE.png',fake_profile)
            z.writestr('00_README_KR.txt','시안 검수용 RC\n이번 기획의 겨울 나온이 독립 원화는 아직 품질 기준 충족 전이므로 이 RC 패키지에 포함하지 않았습니다.')
            for group in ('02_PC_16x9','03_PC_21x9','04_MOBILE_9x16'):
                for i in range(6): z.writestr(f'{group}/TEST_{i}.png',tiny_png())
        winter={k:tiny_png() for k in [*p.TARGETS,p.ORIGINAL_KEY]}
        result=p.write_package(src,out,winter,False)
        self.assertEqual(result['png_count'],23)
        with ZipFile(out) as z:
            self.assertIn(p.ORIGINAL_KEY,z.namelist())
            self.assertEqual(len([x for x in z.namelist() if x.endswith('.png')]),23)

    def test_preview_and_ratios_keep_original_safe(self):
        master=self.make_master()
        before=p.sha256_file(master)
        p.make_preview(master,self.root/'previews')
        self.assertEqual(before,p.sha256_file(master))
        with Image.open(self.root/'previews/WINTER_PC_LAYOUT_PREVIEW.jpg') as im:
            self.assertEqual(im.size,(1280,720))
        with Image.open(self.root/'previews/WINTER_MOBILE_LAYOUT_PREVIEW.jpg') as im:
            self.assertEqual(im.size,(540,960))

    def test_package_readme_and_profile_integrity(self):
        # Synthetic in-memory source ZIP. The test never modifies actual RC/approved source.
        profile=tiny_png();original_profile=p.PROFILE_SHA
        p.PROFILE_SHA=hashlib.sha256(profile).hexdigest()
        self.addCleanup(setattr,p,'PROFILE_SHA',original_profile)
        src=self.root/'synthetic_input.zip';out=self.root/'synthetic_output.zip'
        with ZipFile(src,'w',ZIP_DEFLATED) as z:
            z.writestr('NAON2_PROFILE_GUIDE.png',profile)
            z.writestr('00_README_KR.txt','시안 검수용 RC\n이번 기획의 겨울 나온이 독립 원화는 아직 품질 기준 충족 전이므로 이 RC 패키지에 포함하지 않았습니다.')
            for i in range(45):z.writestr(f'01_ORIGINAL_ARTWORKS/TEST_{i}.png',tiny_png())
        additions={k:tiny_png() for k in (*p.TARGETS,p.LOCK_KEY,p.ORIGINAL_KEY)}
        report=p.write_package(src,out,additions,True)
        self.assertEqual(report['png_count'],51)
        self.assertEqual(report['crc'],'PASS')
        with ZipFile(out) as z:
            self.assertEqual(hashlib.sha256(z.read('NAON2_PROFILE_GUIDE.png')).hexdigest(),p.PROFILE_SHA)
            self.assertIn(p.ORIGINAL_KEY,z.namelist())
            self.assertNotIn('아직 품질 기준',z.read('00_README_KR.txt').decode('utf-8'))
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):
            p.write_package(src,out,additions,True)

    def test_listing_pages_include_real_winter_and_correct_size(self):
        """Rendering checks use labeled synthetic fixtures, never a buyer ZIP."""
        master=self.make_master()
        base=self.root/'seller_fake_base.zip'
        with ZipFile(base,'w') as z:
            for i in range(6):z.writestr(f'02_PC_16x9/TEST_THEME_{i}.png',tiny_png())
        names=p.seller_pages(base,tiny_png(),master,self.root/'seller_pages',False)
        self.assertEqual(len(names),5)
        with Image.open(self.root/'seller_pages/01_MAIN_652x488.jpg') as im:
            self.assertEqual(im.size,(652,488))
        with Image.open(self.root/'seller_pages/05_WINTER_1200x1500.jpg') as im:
            self.assertEqual(im.size,(1200,1500))

    def test_reject_unsafe_zip(self):
        f=self.root/'path_traversal.zip'
        with ZipFile(f,'w') as z:z.writestr('../escape.png',tiny_png())
        with ZipFile(f) as z:
            with self.assertRaisesRegex(ValueError,'Unsafe'):
                p.safe_members(z)

    def test_reject_base_changed(self):
        f=self.root/'invalid_base.zip'
        with ZipFile(f,'w') as z:z.writestr('fake.png',tiny_png())
        with self.assertRaisesRegex(ValueError,'ZIP changed'):
            p.check_base(f,'full')

if __name__=='__main__':unittest.main(verbosity=2)
