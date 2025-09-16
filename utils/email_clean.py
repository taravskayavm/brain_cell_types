from __future__ import annotations

from email_validator import EmailNotValidError, validate_email
import idna
import re

_TLD_RE = r"(?:[A-Za-z]{2,24})"
_TAIL_CUT = re.compile(rf"^(.+?\.(?:{_TLD_RE}))([>\)\]:;,\s].*)$")


def _trim_after_tld(addr: str) -> str:
    """Обрезает хвосты после корректного TLD: '>: ] ) , ;' и пробел."""
    m = _TAIL_CUT.match(addr)
    return m.group(1) if m else addr


_STRIP_CHARS = "\'\"<>[](){}"
_TRAIL_PUNCT = "."


def sanitize_email(addr: str) -> tuple[str, str | None]:
    """Простая очистка e-mail от обрамляющих символов и хвостов."""
    candidate = (addr or "").strip()
    if not candidate:
        return "", "empty"
    candidate = candidate.strip(_STRIP_CHARS)
    candidate = _trim_after_tld(candidate)
    candidate = candidate.rstrip(_TRAIL_PUNCT)
    return candidate, (None if candidate else "empty")


def normalize_domain_idna(domain: str) -> tuple[bool, str, str | None]:
    """
    Приводит домен к нижнему регистру и, при необходимости, к Punycode.
    Возвращает (ok, normalized, reason|None).
    """
    try:
        d = (domain or "").strip().lower()
        if not d or len(d) > 253:
            return False, "", "invalid-domain-length"
        labels = d.split(".")
        out_labels: list[str] = []
        for label in labels:
            if not label or len(label) > 63:
                return False, "", "invalid-label-length"
            if any(ord(c) > 127 for c in label):
                label = idna.encode(label).decode("ascii")
            if not re.fullmatch(r"[a-z0-9-]{1,63}", label) or label.startswith("-") or label.endswith("-"):
                return False, "", "invalid-label"
            out_labels.append(label)
        d_norm = ".".join(out_labels)
        if len(out_labels[-1]) < 2 or len(out_labels[-1]) > 24:
            return False, "", "invalid-tld"
        return True, d_norm, None
    except Exception:
        return False, "", "invalid-idna"


def validate_email_syntax(addr: str) -> tuple[bool, str | None]:
    """
    Проверяет e-mail на синтаксис (без DNS/SMPP).
    Возвращает (ok, reason|None).
    """
    try:
        validate_email(addr, allow_smtputf8=False, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, f"invalid-email:{str(e)[:80]}"
