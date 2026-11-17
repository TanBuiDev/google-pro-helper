"""Versioned Windows DPAPI CurrentUser encryption for local configuration.

On disk the entire configuration is a protected JSON envelope. Runtime reads
and writes still use the original dict. Never fall back to plaintext writes.
"""

import base64
import ctypes
from ctypes import wintypes
import json
import os

FORMAT_FIELD = "__gph_secure_format__"
FORMAT_VALUE = "dpapi-current-user-v1"
PAYLOAD_FIELD = "payload"
CRYPTPROTECT_UI_FORBIDDEN = 0x1


class StorageProtectionError(RuntimeError):
    """Configuration could not be encrypted or decrypted safely."""


def _dpapi(data: bytes, *, encrypt: bool) -> bytes:
    if os.name != "nt":
        raise StorageProtectionError(
            "Windows DPAPI is required; plaintext fallback is disabled."
        )

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ("cbData", wintypes.DWORD),
            ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
        ]

    input_buffer = ctypes.create_string_buffer(data)
    in_blob = DATA_BLOB(
        len(data), ctypes.cast(input_buffer, ctypes.POINTER(ctypes.c_ubyte))
    )
    out_blob = DATA_BLOB()
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    blob_ptr = ctypes.POINTER(DATA_BLOB)
    if encrypt:
        proc = crypt32.CryptProtectData
        proc.argtypes = [
            blob_ptr, wintypes.LPCWSTR, blob_ptr, ctypes.c_void_p,
            ctypes.c_void_p, wintypes.DWORD, blob_ptr,
        ]
        proc.restype = wintypes.BOOL
        args = (
            ctypes.byref(in_blob), "Google Pro Helper", None, None,
            None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out_blob),
        )
    else:
        proc = crypt32.CryptUnprotectData
        proc.argtypes = [
            blob_ptr, ctypes.c_void_p, blob_ptr, ctypes.c_void_p,
            ctypes.c_void_p, wintypes.DWORD, blob_ptr,
        ]
        proc.restype = wintypes.BOOL
        args = (
            ctypes.byref(in_blob), None, None, None,
            None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out_blob),
        )
    try:
        if not proc(*args):
            raise StorageProtectionError(
                "Windows DPAPI failed (wrong Windows user, missing key or "
                "corrupt data); Win32 error: " + str(ctypes.get_last_error())
            )
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        if out_blob.pbData:
            kernel32.LocalFree.argtypes = [ctypes.c_void_p]
            kernel32.LocalFree.restype = ctypes.c_void_p
            kernel32.LocalFree(ctypes.cast(out_blob.pbData, ctypes.c_void_p))


def is_protected(value) -> bool:
    return isinstance(value, dict) and FORMAT_FIELD in value


def encode_config(config: dict) -> dict:
    """Encrypt the entire config (including any future/unknown fields)."""
    if not isinstance(config, dict):
        raise TypeError("Configuration must be a dict")
    if is_protected(config):
        raise StorageProtectionError("Refusing to encrypt an existing envelope")
    plaintext = json.dumps(config, ensure_ascii=False, indent=2).encode("utf-8")
    encrypted = _dpapi(plaintext, encrypt=True)
    return {
        FORMAT_FIELD: FORMAT_VALUE,
        PAYLOAD_FIELD: base64.b64encode(encrypted).decode("ascii"),
    }


def decode_config(stored: dict) -> dict:
    """Decode encrypted v1 or recognize plaintext legacy configuration."""
    if not isinstance(stored, dict):
        raise StorageProtectionError("Configuration root must be an object")
    if not is_protected(stored):
        return stored
    if stored.get(FORMAT_FIELD) != FORMAT_VALUE:
        raise StorageProtectionError("Unknown protected configuration format")
    encoded = stored.get(PAYLOAD_FIELD)
    if not isinstance(encoded, str):
        raise StorageProtectionError("Missing encrypted payload")
    try:
        encrypted = base64.b64decode(encoded, validate=True)
        decoded = json.loads(_dpapi(encrypted, encrypt=False).decode("utf-8"))
    except (ValueError, TypeError, UnicodeError) as exc:
        raise StorageProtectionError("Corrupt encrypted configuration") from exc
    if not isinstance(decoded, dict) or is_protected(decoded):
        raise StorageProtectionError("Invalid decrypted configuration")
    return decoded
