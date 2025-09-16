"""Helpers for logging historical email sending statistics."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from emailbot.messaging_utils import canonical_for_history

LOG_FILE = Path(__file__).resolve().parents[1] / "var" / "send_stats.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _append_jsonl(record: Mapping[str, Any]) -> None:
    path = Path(LOG_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False)
        fh.write("\n")


def log_success(email: str, group: str, extra: dict[str, Any] | None = None) -> None:
    rec: dict[str, Any] = {
        "ts": _now_utc().isoformat().replace("+00:00", "Z"),
        "email": (email or "").strip(),
        "to_canon": canonical_for_history(email or ""),
        "group": (group or "").strip().lower(),
        "status": "success",
    }
    if extra:
        rec.update(extra)
    _append_jsonl(rec)


def log_error(
    email: str,
    group: str,
    error: str,
    extra: dict[str, Any] | None = None,
) -> None:
    rec: dict[str, Any] = {
        "ts": _now_utc().isoformat().replace("+00:00", "Z"),
        "email": (email or "").strip(),
        "to_canon": canonical_for_history(email or ""),
        "group": (group or "").strip().lower(),
        "status": "error",
        "error": (error or "").strip(),
    }
    if extra:
        rec.update(extra)
    _append_jsonl(rec)


def log_bounce(
    email: str,
    group: str,
    error: str,
    extra: dict[str, Any] | None = None,
) -> None:
    rec: dict[str, Any] = {
        "ts": _now_utc().isoformat().replace("+00:00", "Z"),
        "email": (email or "").strip(),
        "to_canon": canonical_for_history(email or ""),
        "group": (group or "").strip().lower(),
        "status": "bounce",
        "error": (error or "").strip(),
    }
    if extra:
        rec.update(extra)
    _append_jsonl(rec)


# Legacy compatibility helpers -------------------------------------------------


def summarize_today(*_args: Any, **_kwargs: Any) -> int:  # pragma: no cover
    return 0


def summarize_week(*_args: Any, **_kwargs: Any) -> int:  # pragma: no cover
    return 0


def summarize_month(*_args: Any, **_kwargs: Any) -> int:  # pragma: no cover
    return 0


def summarize_year(*_args: Any, **_kwargs: Any) -> int:  # pragma: no cover
    return 0
