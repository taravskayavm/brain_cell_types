# -*- coding: utf-8 -*-
import re
from unicodedata import normalize

# Невидимые/zero-width
_ZW = r'\u200B-\u200D\u2060\uFEFF'
_ZW_RE = re.compile(f'[{_ZW}]')

# Верхние индексы: цифры и распространённые надстрочные буквы (в т.ч. ᵃᵇᶜ)
_SUP = r'\u00B9\u00B2\u00B3\u2070-\u2079\u1D2C-\u1D61\u1D62-\u1D6A\u1D43\u1D47\u1D9C\u1DA0'

# Начало пункта/контекста: начало строки, пробелы, буллеты/дефисы/маркировка
_BULLET = r'[ \t>•\-\—·*]+'

# Lookahead на email (строго до '@')
_EMAIL_AHEAD = r'(?=[A-Za-z0-9][A-Za-z0-9._%+\-]*@)'

# Разрешённые «токены-сносок»:
#  - a/b/c (как замена 1/2/3 при кривом шрифте/экспорте)
#  - числа 1–99
#  - римские I/V/X/L/C/D/M (часто встречаются в сносках)
#  - OCR-похожие для чисел: l/I→1, O/o/º/°→0, S/$→5, Z/z→2, B→8
_MARKER_TOKEN = r'(?:[abcABC]|[0-9]{1,2}|[ivxlcdmIVXLCDM]{1,6}|[lI]|[Ooº°]|[Ss$]|[Zz]|B)'

# Унифицируем невидимые символы и нормализуем составные глифы
def _norm_text(t: str) -> str:
    t = normalize('NFC', t)
    return _ZW_RE.sub(' ', t)

# 1) Верхнеиндексные маркеры
_RX_SUP = re.compile(
    rf'(?m)(^|{_BULLET}|[\(\[])[{_SUP}]+[ \t\r\n]*{_EMAIL_AHEAD}'
)

# 2) Скобочные [..]/(..) маркеры с любым из допустимых токенов
_RX_BR = re.compile(
    rf'(?m)(^|{_BULLET})(?:\(\s*{_MARKER_TOKEN}\s*\)|\[\s*{_MARKER_TOKEN}\s*\])[ \t\r\n]*{_EMAIL_AHEAD}'
)

# 3) Классические "a)"/"1)"/"a."/"1." — допускаем 0+ пробелов/перевод строки/zero-width до e-mail
_RX_CLASSIC = re.compile(
    rf'(?m)(^|{_BULLET}){_MARKER_TOKEN}(?:\)|\.)[ \t\r\n]*{_EMAIL_AHEAD}'
)

# Вспомогательные regex для межстрочных маркеров
_EMAIL_START = re.compile(r'^[ \t]*[A-Za-z0-9][A-Za-z0-9._%+\-]*@')
_LINE_MARKER = re.compile(
    rf'^[ \t]*(?:[{_SUP}]+|(?:\(\s*{_MARKER_TOKEN}\s*\)|\[\s*{_MARKER_TOKEN}\s*\])|(?:{_MARKER_TOKEN}(?:\)|\.)))[ \t]*$'
)


def _drop_prevline_markers(t: str) -> str:
    lines = t.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 < len(lines) and _LINE_MARKER.match(line) and _EMAIL_START.match(lines[i + 1]):
            out.append(lines[i + 1])
            i += 2
        else:
            out.append(line)
            i += 1
    return '\n'.join(out)


def detach_list_markers(text: str) -> str:
    """Удаляет ТОЛЬКО маркер непосредственно перед e-mail."""
    t = _norm_text(text)
    t = _drop_prevline_markers(t)
    for rx in (_RX_SUP, _RX_BR, _RX_CLASSIC):
        t = rx.sub(r'\1', t)
    return t

_EMAIL_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9._%+\-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


def smart_extract_emails(text: str):
    text = detach_list_markers(text)
    return _EMAIL_RE.findall(text)
