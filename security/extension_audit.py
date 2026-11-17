"""Non-executing Chrome extension manifest and static script audit."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HOSTS = {
    "https://one.google.com/*",
    "https://play.google.com/*",
    "https://tokenized.play.google.com/*",
}
EXPECTED_SCRIPTS = {
    "content.js": {"matches": ["https://one.google.com/*"], "world": "ISOLATED", "frames": False},
    "inject.js": {"matches": ["https://one.google.com/*"], "world": "MAIN", "frames": False},
    "play_guard.js": {"matches": ["https://tokenized.play.google.com/*"], "world": "MAIN", "frames": True},
}
# Flag introduction of obvious exfiltration / broad browser API primitives.
# The existing XMLHttpRequest.prototype.send interceptor is intentionally
# unchanged and is NOT proof that the checkout flow is safe.
DANGEROUS = {
    "direct network fetch": r"\bfetch\s*\(",
    "new xhr network request": r"\.open\s*\(\s*['\"](?:GET|POST|PUT|PATCH|DELETE)['\"]",
    "beacon": r"\bsendBeacon\s*\(",
    "websocket": r"\bnew\s+WebSocket\s*\(",
    "cookie access": r"\bdocument\.cookie\b|\bchrome\.cookies\b",
    "dynamic code execution": r"\beval\s*\(|\bnew\s+Function\s*\(",
    "native messaging": r"\bchrome\.runtime\.connectNative\s*\(",
    "debugger API": r"\bchrome\.debugger\b",
}


def audit_extension(root=ROOT):
    root = Path(root)
    ext = root / "extension"
    problems = []
    try:
        manifest = json.loads((ext / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["Không đọc được manifest.json: " + type(exc).__name__]
    if manifest.get("manifest_version") != 3:
        problems.append("Extension phải sử dụng Manifest V3.")
    if set(manifest.get("permissions", [])) != {"storage"}:
        problems.append("Quyền extension bị thay đổi; cần duyệt thủ công.")
    if set(manifest.get("host_permissions", [])) != EXPECTED_HOSTS:
        problems.append("host_permissions không trùng danh sách đã duyệt.")
    if manifest.get("background") or manifest.get("externally_connectable"):
        problems.append("Có thành phần nền hoặc kết nối bên ngoài mới.")
    scripts = manifest.get("content_scripts", [])
    if len(scripts) != len(EXPECTED_SCRIPTS):
        problems.append("Số lượng content_scripts thay đổi.")
    seen = set()
    for script in scripts:
        js = script.get("js", [])
        if len(js) != 1 or js[0] not in EXPECTED_SCRIPTS:
            problems.append("Content script mới hoặc không hợp lệ.")
            continue
        name = js[0]
        if name in seen:
            problems.append("Content script bị khai báo trùng.")
        seen.add(name)
        spec = EXPECTED_SCRIPTS[name]
        if script.get("matches") != spec["matches"]:
            problems.append("Phạm vi host của " + name + " đã thay đổi.")
        if script.get("world", "ISOLATED") != spec["world"]:
            problems.append("Chế độ world của " + name + " đã thay đổi.")
        if script.get("all_frames", False) != spec["frames"]:
            problems.append("Phạm vi iframe của " + name + " đã thay đổi.")
    for name in (*EXPECTED_SCRIPTS, "popup.js"):
        try:
            content = (ext / name).read_text(encoding="utf-8")
        except OSError:
            problems.append("Không đọc được " + name)
            continue
        for description, pattern in DANGEROUS.items():
            if re.search(pattern, content, re.IGNORECASE):
                problems.append(name + ": " + description)
    for name in ("popup.html",):
        try:
            content = (ext / name).read_text(encoding="utf-8")
            if re.search(r"<script[^>]+src\s*=\s*['\"]?https?://", content, re.IGNORECASE):
                problems.append(name + ": script tải từ bên ngoài")
        except OSError:
            problems.append("Không đọc được " + name)
    return problems


def main():
    parser = argparse.ArgumentParser(description="Rà soát cấu hình/quyền Chrome Extension mà không chạy tiện ích")
    parser.parse_args()
    problems = audit_extension()
    for problem in problems:
        print("CẢNH BÁO:", problem)
    if problems:
        raise SystemExit(1)
    print("Extension: manifest, quyền truy cập và dấu hiệu mạng/cookie mới chưa thay đổi.")


if __name__ == "__main__":
    main()
