"""Unit tests for conservative screenshot retention with temporary files."""

import importlib.util
from pathlib import Path
import os
import tempfile
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "maintenance.py"


class ScreenshotRetentionTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("_gph_maintenance", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)

    def create(self, name, *, age_days):
        target = self.folder / name
        target.write_bytes(b"test fixture")
        old = time.time() - age_days * 86400
        os.utime(target, (old, old))
        return target

    def test_only_unreferenced_old_png_files_selected(self):
        old = self.create("old.png", age_days=90)
        active = self.create("active.png", age_days=90)
        self.create("new.png", age_days=1)
        self.create("note.txt", age_days=90)
        result = self.module.find_old_screenshots(
            self.folder, keep={"active.png"}, days=30
        )
        self.assertEqual(result, [old])
        self.assertTrue(active.exists())
        self.assertTrue(old.exists())  # the candidate function never deletes

    def test_invalid_retention_is_rejected(self):
        with self.assertRaises(ValueError):
            self.module.find_old_screenshots(self.folder, days=0)


if __name__ == "__main__":
    unittest.main()
