"""Regression coverage for C1 read-only security audits; no network or real data."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


network = load_module("_gph_network_inventory", "security/network_inventory.py")
extension = load_module("_gph_extension_audit", "security/extension_audit.py")
legacy = load_module("_gph_legacy_config_scan", "security/legacy_config_scan.py")


class NetworkAuditTests(unittest.TestCase):
    def test_current_known_hosts_match_reviewed_baseline(self):
        unknown, missing, found = network.compare()
        self.assertEqual(unknown, [])
        self.assertEqual(missing, [])
        self.assertIn("api.floppydata.net", found)
        self.assertIn("geo.g-w.info", found)

    def test_introduced_domain_is_reported_without_url_token(self):
        with tempfile.TemporaryDirectory() as folder:
            dst = Path(folder)
            for relative in network.SOURCE_PATHS:
                out = dst / relative
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, out)
            with (dst / "extension/popup.js").open("a", encoding="utf-8") as out:
                out.write('\n// fixture https://collector.example.net/path?token=TEST-PRIVATE\n')
            unknown, _missing, _found = network.compare(dst)
            self.assertEqual(unknown, ["collector.example.net"])
            self.assertNotIn("TEST-PRIVATE", repr(unknown))


class ExtensionAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        ext = self.root / "extension"
        ext.mkdir()
        for name in ("manifest.json", "popup.html", *extension.EXPECTED_SCRIPTS):
            shutil.copyfile(ROOT / "extension" / name, ext / name)

    def test_current_extension_passes_passive_checks(self):
        self.assertEqual(extension.audit_extension(self.root), [])

    def test_new_host_permission_is_flagged(self):
        path = self.root / "extension/manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["host_permissions"].append("https://example.net/*")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("host_permissions" in e for e in extension.audit_extension(self.root)))

    def test_new_cookie_or_network_access_is_flagged(self):
        path = self.root / "extension/popup.js"
        with path.open("a", encoding="utf-8") as out:
            out.write('\nfetch("https://collector.example.net/"); document.cookie;\n')
        findings = extension.audit_extension(self.root)
        self.assertTrue(any("direct network fetch" in item for item in findings))
        self.assertTrue(any("cookie access" in item for item in findings))


class LegacyFinderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_does_not_modify_or_print_secrets(self):
        data = {"accounts": [{"password": "NEVER-PRINT-THIS"}]}
        plain = self.root / "config (1).json"
        plain.write_text(json.dumps(data), encoding="utf-8")
        encrypted = self.root / "config.json.dpapi.bak"
        encrypted.write_text(json.dumps({
            "__gph_secure_format__": "dpapi-current-user-v1",
            "payload": "dummy-encrypted",
        }), encoding="utf-8")
        env = self.root / ".env"
        env.write_text("SECRET=NEVER-PRINT-THIS", encoding="utf-8")
        screenshots = self.root / "screenshots"
        screenshots.mkdir()
        (screenshots / "config.json").write_text('{"private": "hidden"}', encoding="utf-8")
        before = {p.name: p.read_bytes() for p in (plain, encrypted, env)}
        results = legacy.scan(self.root)
        self.assertEqual([(x["path"], x["classification"]) for x in results], [
            (".env", "sensitive-file-candidate"),
            ("config (1).json", "possibly-plaintext"),
            ("config.json.dpapi.bak", "dpapi-protected"),
        ])
        self.assertNotIn("NEVER-PRINT-THIS", str(results))
        self.assertEqual({p.name: p.read_bytes() for p in (plain, encrypted, env)}, before)

    def test_does_not_follow_symlinks_when_supported(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "config.json").write_text("{}", encoding="utf-8")
        link = self.root / "linked_config.json"
        try:
            link.symlink_to(outside / "config.json")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks not available")
        self.assertFalse(any(x["path"] == "linked_config.json" for x in legacy.scan(self.root)))


if __name__ == "__main__":
    unittest.main()
