from __future__ import annotations

import re
from typing import Iterable

from emailbot.extraction import detach_list_markers
from emailbot.messaging_utils import canonical_for_history
from utils.email_clean import (
    normalize_domain_idna,
    sanitize_email,
    validate_email_syntax,
)

_LOCAL_PART = r"[^\s<>()\[\],;]+"
_DOMAIN_LABEL = r"[^\s<>()\[\],;@.]+"
_CANDIDATE_RE = re.compile(
    rf"({_LOCAL_PART}@(?:{_DOMAIN_LABEL}\.)+{_DOMAIN_LABEL})",
    re.UNICODE,
)


def _iter_candidates(text: str) -> Iterable[str]:
    cleaned = detach_list_markers(text or "")
    seen: set[str] = set()
    for match in _CANDIDATE_RE.finditer(cleaned):
        cand = match.group(1)
        if cand not in seen:
            seen.add(cand)
            yield cand


def run_pipeline_on_text(text: str) -> tuple[list[str], list[tuple[str, str]]]:
    final: list[str] = []
    dropped: list[tuple[str, str]] = []
    seen_canon: set[str] = set()

    for cand in _iter_candidates(text):
        sanitized, sanitize_reason = sanitize_email(cand)
        if not sanitized:
            dropped.append((cand, sanitize_reason or "sanitize-failed"))
            continue

        local, sep, domain = sanitized.partition("@")
        if not sep or not domain:
            dropped.append((sanitized, "missing-domain"))
            continue

        ok, domain_norm, reason = normalize_domain_idna(domain)
        if not ok:
            dropped.append((sanitized, reason or "invalid-idna"))
            continue

        addr = f"{local}@{domain_norm}"

        ok, reason = validate_email_syntax(addr)
        if not ok:
            dropped.append((sanitized, reason or "invalid-email"))
            continue

        canon = canonical_for_history(addr)
        if canon in seen_canon:
            continue
        seen_canon.add(canon)
        final.append(addr)

    return final, dropped
