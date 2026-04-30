from __future__ import annotations

from bisect import bisect_right
from functools import lru_cache
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


MAIN_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SUBTEST_ORDER = ["vc", "sm", "cb", "rm"]
SUBTEST_COLUMNS = {"vc": "VC", "sm": "SM", "cb": "CB", "rm": "RM"}
AGE_BAND_RE = re.compile(r"^(\d+:\d+\s*-\s*\d+:\d+|\d+\s*-\s*\d+)$")
COMPOSITE_TABLES = {
    "verbal": {"sum": "HA", "qi": "HB", "percentile": "HC", "ic": {"child_90": "HD", "child_95": "HE", "adult_90": "HF", "adult_95": "HG"}},
    "execution": {"sum": "IA", "qi": "IB", "percentile": "IC", "ic": {"child_90": "ID", "child_95": "IE", "adult_90": "IF", "adult_95": "IG"}},
    "total_4": {"sum": "JA", "qi": "JB", "percentile": "JC", "ic": {"child_90": "JD", "child_95": "JE", "adult_90": "JF", "adult_95": "JG"}},
    "total_2": {"sum": "KA", "qi": "KB", "percentile": "KC", "ic": {"child_90": "KD", "child_95": "KE", "adult_90": "KF", "adult_95": "KG"}},
}


def workbook_path() -> Path:
    return Path(__file__).resolve().parents[3] / "CORRECAO.xlsm"


def col_number(col: str) -> int:
    value = 0
    for char in col:
        value = (value * 26) + ord(char) - 64
    return value


def col_name(index: int) -> str:
    chars: list[str] = []
    while index:
        index, rem = divmod(index - 1, 26)
        chars.append(chr(65 + rem))
    return "".join(reversed(chars))


def _read_shared_strings(book: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for si in root.findall(f"{MAIN_NS}si"):
        strings.append("".join((text.text or "") for text in si.iter(f"{MAIN_NS}t")))
    return strings


def _read_sheet_values(book: zipfile.ZipFile, sheet_name: str) -> dict[str, str]:
    strings = _read_shared_strings(book)
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    sheets = {
        sheet.attrib["name"]: "xl/" + rel_map[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        for sheet in workbook.find(f"{MAIN_NS}sheets")
    }
    root = ET.fromstring(book.read(sheets[sheet_name]))
    values: dict[str, str] = {}
    for cell in root.findall(f".//{MAIN_NS}c"):
        ref = cell.attrib["r"]
        cell_type = cell.attrib.get("t")
        value = cell.find(f"{MAIN_NS}v")
        inline_string = cell.find(f"{MAIN_NS}is")
        if value is not None and value.text is not None:
            values[ref] = strings[int(value.text)] if cell_type == "s" else value.text
        elif cell_type == "inlineStr" and inline_string is not None:
            values[ref] = "".join((node.text or "") for node in inline_string.iter(f"{MAIN_NS}t"))
    return values


def _parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def _age_metric(years: int, months: int = 0, days: int = 0) -> int:
    return years * 365 + months * 30 + days


def _age_label_to_metric(label: str) -> int:
    normalized = re.sub(r"\s+", "", label)
    if ":" in normalized:
        start = normalized.split("-")[0]
        years, months = start.split(":")
        return _age_metric(int(years), int(months), 0)
    first = normalized.split("-")[0]
    return _age_metric(int(first), 0, 0)


def _parse_percentile(value: str) -> float | None:
    if not value:
        return None
    cleaned = value.replace(",", ".").replace("<", "").replace(">", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


@lru_cache(maxsize=1)
def load_wasi_norms() -> dict:
    with zipfile.ZipFile(workbook_path()) as book:
        values = _read_sheet_values(book, "WASI-Normas")

    age_bands = []
    age_band_cols = []
    for ref in values:
        if not ref.endswith("9") or not re.match(r"^[A-Z]+9$", ref):
            continue
        match = re.match(r"([A-Z]+)9", ref)
        start_col = match.group(1)
        label = values.get(ref, "")
        if values.get(f"{start_col}10") == "VC" and AGE_BAND_RE.match(label.strip()):
            age_band_cols.append(col_number(start_col))
    age_band_cols = sorted(set(age_band_cols))

    for start_index in age_band_cols:
        start_col = col_name(start_index)
        label = values.get(f"{start_col}9")
        if not label:
            continue
        band = {
            "label": label,
            "start_metric": _age_label_to_metric(label),
            "subtests": {},
        }
        for offset, code in enumerate(SUBTEST_ORDER):
            column = col_name(start_index + offset)
            pairs = []
            for row in range(11, 174):
                t_score = _parse_int(values.get(f"A{row}"))
                raw_value = _parse_int(values.get(f"{column}{row}"))
                if t_score is None or raw_value is None:
                    continue
                pairs.append((raw_value, t_score))
            band["subtests"][code] = pairs
        age_bands.append(band)

    tscore_to_weighted = []
    for row in range(11, 72):
        t_score = _parse_int(values.get(f"GO{row}"))
        weighted = _parse_int(values.get(f"GP{row}"))
        if t_score is None or weighted is None:
            continue
        tscore_to_weighted.append((t_score, weighted))

    composite_tables = {}
    for key, table_columns in COMPOSITE_TABLES.items():
        rows = []
        max_row = 251 if key == "total_4" else 131
        for row in range(11, max_row + 1):
            sum_score = _parse_int(values.get(f"{table_columns['sum']}{row}"))
            qi = _parse_int(values.get(f"{table_columns['qi']}{row}"))
            percentile_display = values.get(f"{table_columns['percentile']}{row}")
            if sum_score is None or qi is None or percentile_display is None:
                continue
            rows.append(
                {
                    "sum_score": sum_score,
                    "qi": qi,
                    "percentile_display": percentile_display,
                    "percentile": _parse_percentile(percentile_display),
                    "ic_child_90": values.get(f"{table_columns['ic']['child_90']}{row}"),
                    "ic_child_95": values.get(f"{table_columns['ic']['child_95']}{row}"),
                    "ic_adult_90": values.get(f"{table_columns['ic']['adult_90']}{row}"),
                    "ic_adult_95": values.get(f"{table_columns['ic']['adult_95']}{row}"),
                }
            )
        composite_tables[key] = rows

    return {
        "age_bands": sorted(age_bands, key=lambda item: item["start_metric"]),
        "tscore_to_weighted": tscore_to_weighted,
        "composites": composite_tables,
    }


def select_age_band(age_metric: int) -> dict:
    bands = load_wasi_norms()["age_bands"]
    starts = [band["start_metric"] for band in bands]
    index = bisect_right(starts, age_metric) - 1
    if index < 0:
        raise ValueError("Idade fora da faixa normativa do WASI.")
    return bands[index]


def _lookup_last_leq(value: int, pairs: list[tuple[int, int]]) -> int:
    keys = [item[0] for item in pairs]
    index = bisect_right(keys, value) - 1
    if index < 0:
        raise ValueError("Valor abaixo da faixa normativa.")
    return pairs[index][1]


def lookup_t_score(subtest: str, raw_score: int, age_metric: int) -> tuple[int, str]:
    band = select_age_band(age_metric)
    pairs = band["subtests"][subtest]
    return _lookup_last_leq(raw_score, pairs), band["label"]


def lookup_weighted_score(t_score: int) -> int:
    return _lookup_last_leq(t_score, load_wasi_norms()["tscore_to_weighted"])


def lookup_composite(scale: str, sum_score: int, *, is_child: bool, confidence_level: str) -> dict:
    rows = load_wasi_norms()["composites"][scale]
    candidates = [row["sum_score"] for row in rows]
    index = bisect_right(candidates, sum_score) - 1
    if index < 0:
        raise ValueError("Soma dos escores T fora da faixa normativa.")
    row = rows[index]
    ic_key = f"ic_{'child' if is_child else 'adult'}_{confidence_level}"
    return {
        "sum_score": row["sum_score"],
        "qi": row["qi"],
        "percentile": row["percentile"],
        "percentile_display": row["percentile_display"],
        "confidence_interval": row[ic_key],
    }
