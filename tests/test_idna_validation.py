import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from pipelines.extract_emails import run_pipeline_on_text


def test_idna_russian_domain_converted():
    raw = "Пишите на info@почта.рф"
    final, dropped = run_pipeline_on_text(raw)
    assert any(e.endswith("@xn--80a1acny.xn--p1ai") for e in final)


def test_invalid_label_rejected():
    raw = "mail me: ivan@exa_mple.com"
    final, dropped = run_pipeline_on_text(raw)
    assert "ivan@exa_mple.com" in [d[0] for d in dropped]
