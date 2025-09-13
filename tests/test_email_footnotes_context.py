import os
import sys
import pathlib

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from emailbot.extraction import smart_extract_emails


@pytest.mark.parametrize(
    "text,expected",
    [
        ("a)alex@mail.ru", "alex@mail.ru"),
        ("(a)\n alex@mail.ru", "alex@mail.ru"),
        ("[a] alex@mail.ru", "alex@mail.ru"),
        ("¹²ᵇalex@mail.ru", "alex@mail.ru"),
        ("a)\u200Balex@mail.ru", "alex@mail.ru"),
        ("l) leo@mail.ru", "leo@mail.ru"),
        ("O) olga@mail.ru", "olga@mail.ru"),
        ("S) sergey@mail.ru", "sergey@mail.ru"),
        ("a)\nlexa@mail.ru", "lexa@mail.ru"),
        ("(1)\n ivan@mail.ru", "ivan@mail.ru"),
    ],
)
def test_markers_removed(text, expected):
    assert smart_extract_emails(text) == [expected]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("aalex@mail.ru", "aalex@mail.ru"),
        ("Россия. belyova@mail.ru", "belyova@mail.ru"),
        ("Вариант а) Хороший. Почта: alex@mail.ru", "alex@mail.ru"),
    ],
)
def test_no_false_positive(text, expected):
    assert smart_extract_emails(text) == [expected]
