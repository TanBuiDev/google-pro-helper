"""Passive inventory of hardcoded external connection destinations.

This is NOT a packet capture or guarantee of runtime egress. Never print URL
query strings, proxy usernames, secrets or request bodies.
"""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = (
    "batch/app.py",
    "batch/automation_engine.py",
    "batch/install-and-start.bat",
    "batch/start-dashboard.bat",
    "extension/manifest.json",
    "extension/content.js",
    "extension/inject.js",
    "extension/play_guard.js",
    "extension/popup.js",
)
BASELINE_PATH = ROOT / "security" / "network_destinations.json"
URL_HOST = re.compile(r"\bhttps?://(?P<host>[a-z0-9.-]+)", re.IGNORECASE)
PROXY_HOST = re.compile(r"@(?P<host>[a-z0-9.-]+\.[a-z]{2,}):\d{2,5}\b", re.IGNORECASE)
LOCAL_ONLY = {"localhost", "127.0.0.1", "[::1]"}
DOC_PLACEHOLDERS = {"user", "host", "example.com", "example.invalid"}


def discover_hosts(root=ROOT):
    """Return hostnames only. Do not collect or log URLs, tokens or credentials."""
    found = set()
    root = Path(root)
    for relative in SOURCE_PATHS:
        text = (root / relative).read_text(encoding="utf-8")
        for pattern in (URL_HOST, PROXY_HOST):
            found.update(match.group("host").lower().rstrip(".") for match in pattern.finditer(text))
    return found - DOC_PLACEHOLDERS


def read_baseline(path=BASELINE_PATH):
    entries = json.loads(Path(path).read_text(encoding="utf-8"))["destinations"]
    return {item["host"] for item in entries}


def compare(root=ROOT, baseline=BASELINE_PATH):
    hosts = discover_hosts(root)
    allowed = read_baseline(baseline)
    return sorted(hosts - allowed), sorted(allowed - hosts), sorted(hosts)


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra các domain cố định trong mã nguồn (không kết nối mạng)")
    parser.add_argument("--check", action="store_true", help="Báo lỗi khi có domain mới chưa được duyệt")
    args = parser.parse_args()
    unknown, missing, hosts = compare()
    print("Các domain phát hiện (chỉ tên host, không chứa token/tham số):")
    for host in hosts:
        print(" - " + host + (" [MỚI]" if host in unknown else ""))
    if missing:
        print("Host trong danh sách chuẩn nhưng không còn thấy:", ", ".join(missing))
    if unknown:
        print("CẢNH BÁO: Domain mới cần kiểm tra:", ", ".join(unknown))
    if args.check and unknown:
        raise SystemExit(1)
    print(f"Đã quét tĩnh {len(SOURCE_PATHS)} file; không phải kết quả quan sát lưu lượng thực tế.")


if __name__ == "__main__":
    main()
