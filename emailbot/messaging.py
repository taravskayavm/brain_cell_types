import csv
from datetime import datetime, timezone
from pathlib import Path

SENT_LOG = Path(__file__).with_name("sent_log.csv")


def log_sent_email(to: str, subject: str, status: str, error_msg: str = "") -> None:
    """Append information about email sending to CSV log."""
    row = {
        "last_sent_at": datetime.now(timezone.utc).isoformat(),
        "to": to,
        "subject": subject,
        "status": status,
        "error_msg": error_msg,
    }
    exists = SENT_LOG.exists()
    with SENT_LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(row)
