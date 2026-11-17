"""Explicit, dry-run-by-default cleanup for old screenshots only.

Never cleans Chrome profiles, configuration files, or referenced screenshots.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

import secure_storage

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"


def protected_names(config_path=CONFIG_PATH):
    if not config_path.is_file():
        return set()
    with config_path.open("r", encoding="utf-8") as handle:
        config = secure_storage.decode_config(json.load(handle))
    return {
        Path(account["last_screenshot"]).name
        for account in config.get("accounts", [])
        if isinstance(account, dict) and account.get("last_screenshot")
    }


def find_old_screenshots(folder=SCREENSHOTS_DIR, *, keep=(), days=30, now=None):
    """Return only old, regular PNG files not referenced by any account."""
    if days < 1:
        raise ValueError("Retention must be at least one day")
    folder = Path(folder)
    if not folder.is_dir():
        return []
    threshold = (time.time() if now is None else now) - days * 86400
    keep = set(keep)
    candidates = []
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.name in keep or not entry.name.lower().endswith(".png"):
                continue
            if not entry.is_file(follow_symlinks=False):
                continue
            if entry.stat(follow_symlinks=False).st_mtime < threshold:
                candidates.append(folder / entry.name)
    return sorted(candidates)


def backup_encrypted_config(config_path=CONFIG_PATH):
    """Create an atomic backup of an already encrypted, decryptable config."""
    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as src:
        envelope = json.load(src)
    if not secure_storage.is_protected(envelope):
        raise secure_storage.StorageProtectionError(
            "Please start the application to migrate plaintext config before backup."
        )
    secure_storage.decode_config(envelope)  # Fail closed on corrupt/foreign-user blobs.
    destination = config_path.with_name(config_path.name + ".dpapi.bak")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=config_path.parent, prefix=".config-backup-",
            suffix=".tmp", delete=False,
        ) as tmp, config_path.open("rb") as src:
            temp_path = tmp.name
            shutil.copyfileobj(src, tmp)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(temp_path, destination)
    finally:
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
    return destination


def main():
    parser = argparse.ArgumentParser(description="Dọn ảnh chụp cũ (mặc định chỉ xem trước)")
    parser.add_argument("--days", type=int, default=30, help="Số ngày giữ ảnh (mặc định 30)")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--apply", action="store_true", help="Thực hiện xóa sau khi xem trước")
    actions.add_argument("--backup-config", action="store_true", help="Sao lưu cấu hình đã mã hóa")
    args = parser.parse_args()
    if args.backup_config:
        backup_encrypted_config()
        print("Đã tạo bản sao lưu DPAPI (cùng tài khoản Windows mới giải mã được).")
        return

    # Fail closed when the config cannot be decrypted: never delete an active proof.
    keep = protected_names()
    files = find_old_screenshots(keep=keep, days=args.days)
    if not args.apply:
        print(f"Chế độ xem trước: tìm thấy {len(files)} ảnh cũ có thể xóa.")
        print("Dùng --apply để xác nhận xóa. Ảnh đang được tài khoản tham chiếu được giữ lại.")
        return
    removed = 0
    for file in files:
        if file.is_symlink():
            continue
        file.unlink()
        removed += 1
    print(f"Đã xóa {removed} ảnh cũ. Không xóa hồ sơ trình duyệt và cấu hình.")


if __name__ == "__main__":
    main()
