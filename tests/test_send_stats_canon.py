import json

from emailbot.messaging_utils import canonical_for_history
from utils import send_stats


def test_log_success_includes_canon(tmp_path, monkeypatch):
    log_path = tmp_path / "stats.jsonl"
    monkeypatch.setattr(send_stats, "LOG_FILE", str(log_path))

    send_stats.log_success("user.name+tag@gmail.com", group="test")

    lines = log_path.read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[0])
    assert rec["email"] == "user.name+tag@gmail.com"
    assert rec["to_canon"] == canonical_for_history("user.name+tag@gmail.com")
