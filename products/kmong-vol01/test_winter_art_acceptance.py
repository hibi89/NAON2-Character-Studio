#!/usr/bin/env python3
"""Synthetic fixture tests only — never represents user approval of real character art."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from winter_art_acceptance import check,REQUIRED,PROFILE_SHA,digest

class WinterGateTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.dir=Path(self.tmp.name)
  self.master=self.dir/"TEST_ONLY_PLACEHOLDER.png"
  Image.new("RGB",(2048,2048),"#44338c").save(self.master)
 def fixture(self):
  data={x:True for x in REQUIRED}
  data.update(winter_master_sha256=digest(self.master),
   profile_sheet_sha256=PROFILE_SHA,reviewed_by="user",
   source_provenance="TEST FIXTURE ONLY",rights_basis="TEST FIXTURE ONLY")
  f=self.dir/"TEST_APPROVAL_ONLY.json"
  f.write_text(json.dumps(data),encoding="utf-8")
  return f
 def test_missing_approval_blocked(self):
  r=check(self.master,None)
  self.assertFalse(r["approved"])
 def test_wrong_master_size_blocked(self):
  Image.new("RGB",(1000,1000)).save(self.master)
  self.assertFalse(check(self.master,self.fixture())["approved"])
 def test_wrong_sha_blocked(self):
  f=self.fixture()
  data=json.loads(f.read_text())
  data["winter_master_sha256"]="WRONG"
  f.write_text(json.dumps(data))
  self.assertFalse(check(self.master,f)["approved"])
 def test_unapproved_leg_check_blocked(self):
  f=self.fixture()
  data=json.loads(f.read_text())
  data["exactly_four_legs_visual_qa"]=False
  f.write_text(json.dumps(data))
  self.assertFalse(check(self.master,f)["approved"])
 def test_complete_synthetic_fixture_passes_contract_only(self):
  self.assertTrue(check(self.master,self.fixture())["approved"])
 def test_missing_master_blocked(self):
  self.assertFalse(check(self.dir/"none.png",None)["approved"])
if __name__=="__main__":unittest.main(verbosity=2)
