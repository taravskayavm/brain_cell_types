"""Utility helpers for working with email addresses."""

from __future__ import annotations


def canonical_for_history(email: str) -> str:
    """Return a canonical representation of an email address.

    The helper is intentionally conservative: it normalizes whitespace and
    casing for every domain but applies Gmail-specific canonicalization rules
    so that addresses like ``username+tag@gmail.com`` and ``username@gmail.com``
    are treated as the same entity when analysing historical logs.
    """

    if not email:
        return ""

    normalized = email.strip().lower()
    if "@" not in normalized:
        return normalized

    local_part, _, domain = normalized.partition("@")
    if not local_part or not domain:
        return normalized

    if domain in {"gmail.com", "googlemail.com"}:
        local_part = local_part.split("+", 1)[0]
        local_part = local_part.replace(".", "")
        domain = "gmail.com"

    return f"{local_part}@{domain}"
