import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - fallback when zoneinfo missing
    ZoneInfo = None

SENT_LOG = Path(__file__).with_name("sent_log.csv")

_SUCCESS_STATUSES = {"ok", "sent", "success"}


def _get_tz():
    tz_name = os.getenv("REPORT_TZ", "Europe/Moscow")
    if ZoneInfo is None:
        return timezone.utc
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return timezone.utc


def get_report(period: str) -> str:
    tz = _get_tz()
    now_local = datetime.now(tz)
    if period == "day":
        start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = (now_local - timedelta(days=now_local.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    elif period == "month":
        start = now_local - timedelta(days=30)
    elif period == "year":
        start = now_local - timedelta(days=365)
    else:
        raise ValueError(f"Unknown period: {period}")

    cnt_ok = 0
    cnt_err = 0

    if SENT_LOG.exists():
        with SENT_LOG.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row.get("last_sent_at") or ""
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    dt = dt.astimezone(tz)
                except Exception:
                    continue
                if not (start <= dt <= now_local):
                    continue
                status = (row.get("status") or "").lower()
                if status in _SUCCESS_STATUSES:
                    cnt_ok += 1
                else:
                    cnt_err += 1

    return f"Успешных: {cnt_ok}\nОшибок: {cnt_err}"
