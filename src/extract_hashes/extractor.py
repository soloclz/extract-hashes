"""Hash candidate extraction and structural classification."""

from __future__ import annotations


HEX_LENGTHS = {
    32: "MD5, MD4, NTLM, or another 128-bit format",
    40: "SHA-1, RIPEMD-160, or another 160-bit format",
    56: "SHA-224 or another 224-bit format",
    64: "SHA-256 or another 256-bit format",
    96: "SHA-384 or another 384-bit format",
    128: "SHA-512 or another 512-bit format",
}


def extract(text: str) -> list[str]:
    """Return unique hexadecimal candidates in first-seen order."""
    candidates: list[str] = []
    seen: set[str] = set()
    token: list[str] = []

    def accept() -> None:
        if len(token) not in HEX_LENGTHS:
            token.clear()
            return
        value = "".join(token).lower()
        token.clear()
        if value not in seen:
            seen.add(value)
            candidates.append(value)

    for character in text:
        if character in "0123456789abcdefABCDEF":
            token.append(character)
        else:
            accept()
    accept()
    return candidates
