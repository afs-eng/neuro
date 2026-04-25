from __future__ import annotations

import csv
import json
from pathlib import Path

from .constants import (
    WAIS3_COMPOSITE_TABLES,
    WAIS3_PSYCHOMETRICS_TABLES,
    WAIS3_SUPPLEMENTARY_TABLES,
    WAIS3_VERBAL_SUBTESTS,
    classify_composite_score,
)
from .norm_utils import has_meaningful_value, normalize_csv_value, raw_score_matches_interval


class WAIS3NormLoader:
    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or Path(__file__).resolve().parent / "tabelas"

    def load_manifest(self) -> dict:
        manifest_path = self.base_path / "metadata" / "wais3_tables_manifest.json"
        if not manifest_path.exists():
            return {}
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def get_scaled_score(self, subtest_key: str, raw_score: int, age_range_key: str) -> int:
        domain = "verbal" if subtest_key in WAIS3_VERBAL_SUBTESTS else "execucao"
        path = self.base_path / "raw_to_scaled" / domain / f"{age_range_key}.csv"
        rows = self._read_csv_rows(path)
        # If the normative file exists but contains no meaningful values (only headers),
        # fall back to the template conversion file for the domain/age.
        skip_cols = {"tabela", "faixa_etaria", "tipo_subteste", "escore_ponderado"}
        if not rows or not self._rows_have_meaningful_values(rows, skip_columns=skip_cols):
            template_path = self.base_path / "conversao_bruto_ponderado_templates" / domain / f"{age_range_key}_{domain}.csv"
            template_rows = self._read_csv_rows(template_path)
            if template_rows and self._rows_have_meaningful_values(template_rows, skip_columns=skip_cols):
                rows = template_rows
                path = template_path
        if not rows:
            raise ValueError(f"Tabela normativa vazia ou ausente: {path.name}")
        if subtest_key not in rows[0]:
            raise ValueError(f"Subteste não encontrado na tabela: {subtest_key}")
        for row in rows:
            if raw_score_matches_interval(raw_score, row.get(subtest_key)):
                score = normalize_csv_value(row.get("escore_ponderado"))
                if score is not None:
                    return int(score)
        raise ValueError(
            f"Não foi encontrada conversão para {subtest_key}, bruto={raw_score}, faixa={age_range_key}"
        )

    def get_composite_score(self, index_key: str, scaled_sum: int) -> dict:
        spec = WAIS3_COMPOSITE_TABLES.get(index_key)
        if spec:
            rows = self._read_csv_rows(self.base_path / spec["path"])
            if rows:
                for row in rows:
                    if normalize_csv_value(row.get(spec["sum_column"])) == scaled_sum:
                        score = normalize_csv_value(row.get(spec["score_column"]))
                        if score is None:
                            raise ValueError(
                                f"Linha encontrada para {index_key} com valor normativo ausente na soma {scaled_sum}"
                            )
                        return {
                            "pontuacao_composta": score,
                            "percentil": normalize_csv_value(row.get(spec["percentile_column"])),
                            "ic_90": row.get(spec["ic90_column"]) or None,
                            "ic_95": row.get(spec["ic95_column"]) or None,
                            "classificacao": classify_composite_score(int(score)),
                            "source": spec["path"],
                        }

        path = self.base_path / "composite_scores" / f"{index_key}.csv"
        rows = self._read_csv_rows(path)
        if not rows:
            raise ValueError(f"Tabela composta vazia ou ausente: {path.name}")
        for row in rows:
            if normalize_csv_value(row.get("soma_ponderada")) == scaled_sum:
                score = normalize_csv_value(row.get("pontuacao_composta"))
                if score is None:
                    raise ValueError(
                        f"Linha encontrada para {index_key} com valor normativo ausente na soma {scaled_sum}"
                    )
                return {
                    "pontuacao_composta": score,
                    "percentil": normalize_csv_value(row.get("percentil")),
                    "ic_90": row.get("ic_90") or None,
                    "ic_95": row.get("ic_95") or None,
                    "classificacao": row.get("classificacao") or classify_composite_score(int(score)),
                    "source": f"composite_scores/{index_key}.csv",
                }
        raise ValueError(f"Soma ponderada não encontrada para {index_key}: {scaled_sum}")

    def get_supplementary_tables(self) -> dict[str, list[dict[str, str]]]:
        return {
            key: rows
            for key, rows in (
                (key, self._read_csv_rows(self.base_path / relative_path))
                for key, relative_path in WAIS3_SUPPLEMENTARY_TABLES.items()
            )
            if rows
        }

    def get_psychometrics_tables(self) -> dict[str, list[dict[str, str]]]:
        return {
            key: rows
            for key, rows in (
                (key, self._read_csv_rows(self.base_path / relative_path))
                for key, relative_path in WAIS3_PSYCHOMETRICS_TABLES.items()
            )
            if rows
        }

    def has_normative_data(self) -> bool:
        return self.has_scaled_score_data() and self.has_composite_data()

    def has_scaled_score_data(self) -> bool:
        sample_files = [
            self.base_path / "raw_to_scaled" / "verbal" / "idade_16-17.csv",
            self.base_path / "raw_to_scaled" / "execucao" / "idade_16-17.csv",
            self.base_path / "conversao_bruto_ponderado_templates" / "verbal" / "idade_16-17_verbal.csv",
            self.base_path / "conversao_bruto_ponderado_templates" / "execucao" / "idade_16-17_execucao.csv",
        ]
        return any(self._rows_have_meaningful_values(self._read_csv_rows(path), skip_columns={"tabela", "faixa_etaria", "tipo_subteste", "escore_ponderado"}) for path in sample_files)

    def has_composite_data(self) -> bool:
        for spec in WAIS3_COMPOSITE_TABLES.values():
            rows = self._read_csv_rows(self.base_path / spec["path"])
            if self._rows_have_meaningful_values(rows, skip_columns={"tabela", "nome_tabela", spec["sum_column"]}):
                return True
        sample = self._read_csv_rows(self.base_path / "composite_scores" / "qi_total.csv")
        return self._rows_have_meaningful_values(sample, skip_columns={"soma_ponderada"})

    @staticmethod
    def _rows_have_meaningful_values(rows: list[dict[str, str]], skip_columns: set[str]) -> bool:
        for row in rows:
            for key, value in row.items():
                if key in skip_columns:
                    continue
                if has_meaningful_value(value):
                    return True
        return False

    def _read_csv_rows(self, path: Path) -> list[dict[str, str]]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            sample = fh.read(2048)
            fh.seek(0)
            delimiter = ";" if sample.count(";") > sample.count(",") else ","
            return [row for row in csv.DictReader(fh, delimiter=delimiter)]
