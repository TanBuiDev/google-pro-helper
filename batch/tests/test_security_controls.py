"""Security regression tests using only the Python standard library."""

import ast
import asyncio
import hmac
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any, Dict, Optional
import unittest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def load_security_functions():
    source = ast.parse(APP_PATH.read_text(encoding="utf-8"), filename=str(APP_PATH))
    selected = []
    for node in source.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in {
            "redact_sensitive", "protect_local_access",
        }:
            node.decorator_list = []
            selected.append(node)
    globals_ = {
        "Optional": Optional, "Dict": Dict, "Any": Any, "Request": object,
        "re": re, "hmac": hmac,
        "LOCAL_ACCESS_TOKEN": "a-test-session-token",
        "ALLOWED_LOCAL_HOSTS": {"127.0.0.1:8765", "localhost:8765"},
        "ALLOWED_LOCAL_ORIGINS": {"http://127.0.0.1:8765", "http://localhost:8765"},
        "get_totp": lambda secret: "654321",
    }

    class FakeJSONResponse:
        def __init__(self, *, status_code, content):
            self.status_code = status_code
            self.content = content
            self.headers = {}

    globals_["JSONResponse"] = FakeJSONResponse
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(APP_PATH), "exec"), globals_)
    return globals_


class LocalSecurityTests(unittest.TestCase):
    def setUp(self):
        self.fn = load_security_functions()

    def request(self, path="/api/state", host="127.0.0.1:8765",
                origin=None, token=None):
        headers = {"host": host}
        if origin is not None:
            headers["origin"] = origin
        if token is not None:
            headers["x-gph-local-token"] = token
        return SimpleNamespace(headers=headers, url=SimpleNamespace(path=path))

    def call_middleware(self, request):
        async def next_handler(_request):
            return SimpleNamespace(status_code=200, headers={})
        return asyncio.run(self.fn["protect_local_access"](request, next_handler))

    def test_rejects_untrusted_hosts_origins_and_missing_token(self):
        examples = [
            self.request(host="attacker.test:8765", token="a-test-session-token"),
            self.request(origin="https://attacker.test", token="a-test-session-token"),
            self.request(),
            self.request(token="wrong-token"),
            self.request(path="/screenshots/proof.png"),
        ]
        for request in examples:
            with self.subTest(headers=request.headers, path=request.url.path):
                self.assertEqual(self.call_middleware(request).status_code, 403)

    def test_allows_local_token_and_does_not_cache_responses(self):
        response = self.call_middleware(self.request(token="a-test-session-token"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        screenshot = self.call_middleware(self.request(
            path="/screenshots/proof.png", token="a-test-session-token",
            origin="http://127.0.0.1:8765"
        ))
        self.assertEqual(screenshot.status_code, 200)

    def test_redacts_password_totp_card_and_proxy_credentials(self):
        cfg = {
            "accounts": [{"password": "sample-private-password", "totp_secret": "totp-secret"}],
            "card": {"number": "4111111111111111"},
            "proxy_template": "http://user:proxy-password@proxy.example:8080",
        }
        value = (
            "sample-private-password totp-secret 654321 4111111111111111 "
            "CVC: 123 http://user:proxy-password@proxy.example:8080"
        )
        redacted = self.fn["redact_sensitive"](value, cfg)
        for secret in ("sample-private-password", "totp-secret", "654321", 
                       "4111111111111111", "CVC: 123", "proxy-password"):
            with self.subTest(secret=secret):
                self.assertNotIn(secret, redacted)
        self.assertIn("[ĐÃ ẨN]", redacted)


if __name__ == "__main__":
    unittest.main()
