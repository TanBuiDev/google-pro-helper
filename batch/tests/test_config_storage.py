"""Storage/migration regression tests. Fake DPAPI on non-Windows; no live accounts."""

import ast
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


BATCH_DIR = Path(__file__).resolve().parents[1]
APP_PATH = Path(os.environ.get("CONFIG_STORAGE_APP", BATCH_DIR / "app.py"))
SECURE_PATH = BATCH_DIR / "secure_storage.py"


def load_storage_functions():
    spec = importlib.util.spec_from_file_location("_gph_secure_storage_test", SECURE_PATH)
    protected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(protected)
    source = ast.parse(APP_PATH.read_text(encoding="utf-8"), filename=str(APP_PATH))
    nodes = []
    for node in source.body:
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            nodes.append(node)
        elif isinstance(node, ast.Import) and all(alias.name in {"json", "os", "tempfile"} for alias in node.names):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {"load_config", "save_config"}:
            nodes.append(node)
    namespace = {"secure_storage": protected}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(APP_PATH), "exec"), namespace)
    return namespace


def fake_dpapi(data, *, encrypt):
    if encrypt:
        return b"UNIT-TEST-ONLY:" + data[::-1]
    prefix = b"UNIT-TEST-ONLY:"
    if not data.startswith(prefix):
        raise ValueError("Mock encrypted payload invalid")
    return data[len(prefix):][::-1]


class ConfigStorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "config.json"
        self.storage = load_storage_functions()
        self.storage["CONFIG_PATH"] = str(self.path)
        patcher = mock.patch.object(
            self.storage["secure_storage"], "_dpapi", side_effect=fake_dpapi
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.previous = {
            "accounts": [
                {"id": "existing", "email": "test@example.invalid",
                 "password": "example-private-password", "totp_secret": "ABCDEFGH"}
            ],
            "card": {"number": "4111111111111111", "cvc": "123"},
            "proxy_template": "http://proxy-user:proxy-password@proxy.example:8080",
            "unknown_field": ["preserved", 99],
        }
        self.path.write_text(
            json.dumps(self.previous, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.previous_bytes = self.path.read_bytes()

    def assert_untouched(self):
        self.assertEqual(self.path.read_bytes(), self.previous_bytes)
        self.assertEqual(list(self.path.parent.glob(".config-*.tmp")), [])

    def test_legacy_plaintext_is_migrated_and_runtime_format_stays_the_same(self):
        self.assertEqual(self.storage["load_config"](), self.previous)
        contents = self.path.read_text(encoding="utf-8")
        envelope = json.loads(contents)
        self.assertEqual(envelope["__gph_secure_format__"], "dpapi-current-user-v1")
        for sensitive in ("example-private-password", "test@example.invalid",
                          "4111111111111111", "123", "proxy-password", "ABCDEFGH"):
            self.assertNotIn(sensitive, contents)
        self.assertEqual(self.storage["load_config"](), self.previous)
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir()), ["config.json"])

    def test_new_config_round_trip_and_unknown_fields_preserved(self):
        payload = {"accounts": [{"id": "new", "password": "new-secret"}],
                   "auto_cancel": False, "card": {}, "other": {"nested": ["kept"]}}
        self.storage["save_config"](payload)
        self.assertEqual(self.storage["load_config"](), payload)
        self.assertNotIn("new-secret", self.path.read_text(encoding="utf-8"))

    def test_serialization_failure_preserves_original(self):
        with self.assertRaises(TypeError):
            self.storage["save_config"]({"accounts": [], "invalid": object()})
        self.assert_untouched()

    def test_dpapi_encryption_failure_preserves_original(self):
        with mock.patch.object(self.storage["secure_storage"], "_dpapi",
                               side_effect=RuntimeError("DPAPI unavailable")):
            with self.assertRaisesRegex(RuntimeError, "DPAPI unavailable"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_migration_failure_does_not_overwrite_legacy_plaintext(self):
        with mock.patch.object(self.storage["secure_storage"], "_dpapi",
                               side_effect=RuntimeError("DPAPI unavailable")):
            with self.assertRaisesRegex(RuntimeError, "DPAPI unavailable"):
                self.storage["load_config"]()
        self.assert_untouched()

    def test_replace_failure_preserves_original(self):
        with mock.patch.object(os, "replace", side_effect=PermissionError("blocked")):
            with self.assertRaisesRegex(PermissionError, "blocked"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_flush_failure_preserves_original(self):
        with mock.patch.object(os, "fsync", side_effect=OSError("disk failed")):
            with self.assertRaisesRegex(OSError, "disk failed"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_temp_creation_failure_preserves_original(self):
        with mock.patch.object(tempfile, "NamedTemporaryFile",
                               side_effect=PermissionError("creation failed")):
            with self.assertRaisesRegex(PermissionError, "creation failed"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_complete_encrypted_temp_is_swapped_atomically(self):
        original_replace = os.replace

        def checked_replace(source, destination):
            self.assertEqual(Path(source).parent, self.path.parent)
            self.assertEqual(Path(destination), self.path)
            encoded = json.loads(Path(source).read_text(encoding="utf-8"))
            self.assertEqual(self.storage["secure_storage"].decode_config(encoded),
                             {"accounts": [], "notice": "ok"})
            self.assertEqual(self.path.read_bytes(), self.previous_bytes)
            original_replace(source, destination)

        with mock.patch.object(os, "replace", side_effect=checked_replace):
            self.storage["save_config"]({"accounts": [], "notice": "ok"})

    def test_invalid_json_fails_closed(self):
        self.path.write_text("{invalid", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            self.storage["load_config"]()

    def test_corrupt_encrypted_payload_fails_closed_without_overwrite(self):
        self.path.write_text(json.dumps({
            "__gph_secure_format__": "dpapi-current-user-v1",
            "payload": "not-valid-base64!!",
        }), encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaises(self.storage["secure_storage"].StorageProtectionError):
            self.storage["load_config"]()
        self.assertEqual(self.path.read_bytes(), before)

    def test_repeated_updates_leave_no_temporary_files(self):
        for number in range(20):
            self.storage["save_config"]({"accounts": [], "revision": number})
            self.assertEqual(self.storage["load_config"]()["revision"], number)
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir()), ["config.json"])


class RealWindowsDpapiTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "DPAPI is available only on Windows")
    def test_current_user_round_trip(self):
        storage = load_storage_functions()["secure_storage"]
        payload = {"password": "windows-only-test", "nested": {"cvc": "987"}}
        encrypted = storage.encode_config(payload)
        self.assertEqual(storage.decode_config(encrypted), payload)
        self.assertNotIn("windows-only-test", json.dumps(encrypted))


if __name__ == "__main__":
    unittest.main()
