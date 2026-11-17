"""Read-only local finder for legacy configuration and backup files.

This tool never deletes or modifies files, never prints secrets, and never
scans a user's home directory without an explicit --root argument.
"""
import argparse
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "batch"
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "profiles", "screenshots", ".pytest_cache"}
MAX_INSPECT_SIZE = 4 * 1024 * 1024


def is_candidate(name):
    lower = name.lower()
    return bool(re.match(r"^config(?:[ .(_-].*)?\.json(?:\.dpapi\.bak)?$", lower)
                or re.match(r"^\.config-.*\.tmp$", lower)
                or lower == ".env"
                or lower.startswith(".env.")
                or lower.endswith(".dpapi.bak"))


def classify(path):
    """Examine only likely JSON config files; do not expose any field values."""
    if path.stat().st_size > MAX_INSPECT_SIZE:
        return "file-too-large"
    if not path.name.lower().endswith((".json", ".dpapi.bak", ".tmp")):
        return "sensitive-file-candidate"
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, ValueError):
        return "unknown-content"
    if isinstance(value, dict) and value.get("__gph_secure_format__") == "dpapi-current-user-v1":
        return "dpapi-protected"
    return "possibly-plaintext"


def scan(root=ROOT):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Folder not found")
    found = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base = Path(current)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not (base / d).is_symlink()]
        for filename in files:
            path = base / filename
            if not is_candidate(filename) or path.is_symlink() or not path.is_file():
                continue
            found.append({"path": path.relative_to(root).as_posix(), "classification": classify(path)})
    return sorted(found, key=lambda item: item["path"])


def main():
    parser = argparse.ArgumentParser(description="Chỉ phát hiện file cấu hình có thể chứa dữ liệu nhạy cảm; KHÔNG xóa")
    parser.add_argument("--root", type=Path, default=ROOT, help="Thư mục cần kiểm tra (mặc định: batch)")
    args = parser.parse_args()
    results = scan(args.root)
    for item in results:
        print(f"{item['path']}: {item['classification']}")
    print(f"Tìm thấy {len(results)} file cần xem xét. Công cụ KHÔNG xóa, giải mã hay sao chép dữ liệu.")


if __name__ == "__main__":
    main()
