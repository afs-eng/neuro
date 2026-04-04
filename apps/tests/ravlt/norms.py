from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class NormEntry:
    p5: float
    p25: float
    p50: float
    p75: float
    p95: float
    mean: float
    sd: float


NORMS: Dict[str, Dict[str, NormEntry]] = {
    "6-8": {
        "A1": NormEntry(2, 3, 4, 5, 8, 4.5, 1.9),
        "A2": NormEntry(3, 5, 6, 7, 10, 6.0, 2.1),
        "A3": NormEntry(4, 5, 7, 9, 12, 7.0, 2.5),
        "A4": NormEntry(4, 6, 8, 10, 13, 7.9, 2.8),
        "A5": NormEntry(4, 7, 8, 10, 13, 8.4, 2.8),
        "B1": NormEntry(2, 3, 4, 5, 7, 4.3, 1.6),
        "A6": NormEntry(3, 5, 7, 8, 13, 7.2, 2.7),
        "A7": NormEntry(3, 6, 7, 9, 13, 7.6, 2.7),
        "Reconhecimento Lista A": NormEntry(-2, 8, 10, 15, 15, 10.3, 6.9),
        "Escore Total": NormEntry(19, 26, 33, 40, 52, 33.7, 9.9),
        "Aprend. longo das Tentativas": NormEntry(-4, 6, 12, 16, 23, 11.2, 8.2),
        "Velocidade de Esquecimento": NormEntry(
            0.67, 0.89, 1.00, 1.20, 1.75, 1.09, 0.37
        ),
        "Interferência Proativa": NormEntry(0.50, 0.75, 1.00, 1.29, 2.00, 1.09, 0.55),
        "Interferência Retroativa": NormEntry(0.50, 0.71, 0.88, 1.00, 1.25, 0.87, 0.24),
    },
    "9-11": {
        "A1": NormEntry(3, 4, 5, 7, 8, 5.4, 1.8),
        "A2": NormEntry(4, 6, 7, 9, 11, 7.1, 2.2),
        "A3": NormEntry(3, 6, 9, 11, 13, 8.2, 2.8),
        "A4": NormEntry(4, 8, 9, 11, 14, 9.2, 2.8),
        "A5": NormEntry(5, 8, 10, 12, 14, 10.0, 2.7),
        "B1": NormEntry(3, 4, 5, 6, 8, 5.0, 1.5),
        "A6": NormEntry(4, 7, 9, 11, 12, 8.7, 2.7),
        "A7": NormEntry(4, 7, 9, 11, 13, 8.7, 2.7),
        "Reconhecimento Lista A": NormEntry(2, 11, 14, 15, 15, 11.7, 5.5),
        "Escore Total": NormEntry(24, 32, 40, 46, 58, 39.9, 10.1),
        "Aprend. longo das Tentativas": NormEntry(-1, 8, 13, 19, 26, 12.8, 8.1),
        "Velocidade de Esquecimento": NormEntry(
            0.75, 0.90, 1.00, 1.11, 1.33, 1.03, 0.25
        ),
        "Interferência Proativa": NormEntry(0.50, 0.71, 0.86, 1.20, 2.00, 1.00, 0.46),
        "Interferência Retroativa": NormEntry(0.56, 0.73, 0.85, 1.00, 1.38, 0.91, 0.38),
    },
    "12-14": {
        "A1": NormEntry(4, 5, 6, 8, 9, 6.3, 1.7),
        "A2": NormEntry(4, 6, 8, 10, 12, 8.1, 2.6),
        "A3": NormEntry(4, 7, 10, 12, 14, 9.5, 2.9),
        "A4": NormEntry(3, 9, 10, 12, 14, 10.0, 2.7),
        "A5": NormEntry(6, 10, 11, 13, 15, 10.9, 2.5),
        "B1": NormEntry(3, 4, 6, 7, 9, 5.6, 1.7),
        "A6": NormEntry(5, 9, 10, 11, 13, 9.6, 2.2),
        "A7": NormEntry(5, 7, 10, 12, 14, 9.6, 3.0),
        "Reconhecimento Lista A": NormEntry(0, 12, 15, 15, 15, 12.5, 5.0),
        "Escore Total": NormEntry(28, 39, 46, 51, 59, 44.8, 9.6),
        "Aprend. longo das Tentativas": NormEntry(-2, 7, 13, 20, 25, 13.3, 7.8),
        "Velocidade de Esquecimento": NormEntry(
            0.60, 0.89, 1.00, 1.11, 1.40, 1.01, 0.29
        ),
        "Interferência Proativa": NormEntry(0.50, 0.73, 0.88, 1.13, 1.50, 0.92, 0.28),
        "Interferência Retroativa": NormEntry(0.60, 0.80, 0.90, 1.00, 1.22, 0.91, 0.29),
    },
    "15-17": {
        "A1": NormEntry(4, 5, 6, 7, 8, 6.1, 1.4),
        "A2": NormEntry(4, 7, 8, 9, 11, 8.1, 2.2),
        "A3": NormEntry(4, 8, 10, 11, 13, 9.6, 2.4),
        "A4": NormEntry(6, 10, 11, 13, 14, 11.1, 2.4),
        "A5": NormEntry(7, 10, 11, 14, 14, 11.6, 2.3),
        "B1": NormEntry(3, 4, 5, 6, 9, 5.4, 1.7),
        "A6": NormEntry(5, 9, 10, 13, 14, 10.6, 2.5),
        "A7": NormEntry(6, 9, 11, 12, 14, 10.5, 2.9),
        "Reconhecimento Lista A": NormEntry(4, 11, 13, 15, 15, 12.6, 3.1),
        "Escore Total": NormEntry(34, 41, 46, 53, 58, 46.4, 8.6),
        "Aprend. longo das Tentativas": NormEntry(2, 13, 17, 21, 26, 16.1, 7.3),
        "Velocidade de Esquecimento": NormEntry(
            0.79, 0.90, 1.00, 1.11, 1.35, 1.01, 0.25
        ),
        "Interferência Proativa": NormEntry(0.54, 0.69, 0.86, 1.06, 1.42, 0.91, 0.27),
        "Interferência Retroativa": NormEntry(0.64, 0.82, 0.93, 1.00, 1.23, 0.93, 0.17),
    },
    "18-20": {
        "A1": NormEntry(4, 6, 7, 8, 10, 6.8, 1.7),
        "A2": NormEntry(6, 8, 9, 11, 13, 9.5, 2.2),
        "A3": NormEntry(8, 10, 11, 13, 14, 11.0, 2.2),
        "A4": NormEntry(8, 10, 12, 14, 15, 11.8, 2.4),
        "A5": NormEntry(8, 11, 12, 14, 15, 12.2, 2.4),
        "B1": NormEntry(4, 5, 6, 7, 9, 6.3, 1.8),
        "A6": NormEntry(6, 9, 12, 13, 15, 11.1, 2.5),
        "A7": NormEntry(6, 9, 11, 13, 15, 11.0, 2.7),
        "Reconhecimento Lista A": NormEntry(-1, 5, 13, 15, 15, 10.0, 5.7),
        "Escore Total": NormEntry(36, 46, 52, 58, 65, 51.4, 8.7),
        "Aprend. longo das Tentativas": NormEntry(6, 12, 18, 22, 29, 17.3, 7.3),
        "Velocidade de Esquecimento": NormEntry(
            0.75, 0.91, 1.00, 1.10, 1.33, 1.00, 0.20
        ),
        "Interferência Proativa": NormEntry(0.56, 0.73, 0.89, 1.10, 1.50, 0.96, 0.33),
        "Interferência Retroativa": NormEntry(0.63, 0.82, 0.92, 1.00, 1.18, 0.96, 0.68),
    },
    "21-30": {
        "A1": NormEntry(4, 5, 7, 8, 9, 6.5, 1.7),
        "A2": NormEntry(5, 7, 9, 10, 12, 8.9, 2.2),
        "A3": NormEntry(6, 9, 11, 12, 14, 10.4, 2.4),
        "A4": NormEntry(7, 10, 12, 13, 15, 11.4, 2.4),
        "A5": NormEntry(8, 11, 13, 14, 15, 12.2, 2.2),
        "B1": NormEntry(3, 4, 6, 7, 9, 5.7, 1.8),
        "A6": NormEntry(6, 9, 11, 13, 15, 10.9, 2.6),
        "A7": NormEntry(6, 9, 11, 13, 15, 10.7, 2.7),
        "Reconhecimento Lista A": NormEntry(1, 11, 13, 14, 15, 11.4, 4.7),
        "Escore Total": NormEntry(34, 44, 50, 56, 63, 49.3, 8.6),
        "Aprend. longo das Tentativas": NormEntry(5, 13, 17, 21, 27, 16.8, 6.5),
        "Velocidade de Esquecimento": NormEntry(
            0.75, 0.91, 1.00, 1.09, 1.33, 1.00, 0.27
        ),
        "Interferência Proativa": NormEntry(0.50, 0.68, 0.86, 1.00, 1.50, 0.92, 0.37),
        "Interferência Retroativa": NormEntry(0.63, 0.80, 0.91, 1.00, 1.10, 0.89, 0.17),
    },
    "31-40": {
        "A1": NormEntry(4, 5, 6, 7, 9, 6.1, 1.6),
        "A2": NormEntry(5, 7, 9, 10, 12, 8.7, 2.0),
        "A3": NormEntry(6, 9, 10, 12, 14, 10.3, 2.1),
        "A4": NormEntry(7, 10, 11, 13, 15, 11.4, 2.1),
        "A5": NormEntry(8, 11, 12, 14, 15, 12.2, 2.2),
        "B1": NormEntry(2, 4, 5, 6, 8, 5.3, 1.6),
        "A6": NormEntry(6, 9, 11, 12, 14, 10.8, 2.4),
        "A7": NormEntry(6, 9, 11, 12, 14, 10.3, 2.4),
        "Reconhecimento Lista A": NormEntry(-2, 10, 13, 14, 15, 11.1, 4.7),
        "Escore Total": NormEntry(35, 43, 49, 54, 60, 48.6, 8.0),
        "Aprend. longo das Tentativas": NormEntry(6, 14, 18, 23, 29, 17.9, 7.0),
        "Velocidade de Esquecimento": NormEntry(
            0.75, 0.86, 0.93, 1.08, 1.29, 0.97, 0.19
        ),
        "Interferência Proativa": NormEntry(0.50, 0.67, 0.86, 1.00, 1.50, 0.91, 0.33),
        "Interferência Retroativa": NormEntry(0.58, 0.80, 0.91, 0.93, 1.18, 0.94, 0.74),
    },
    "41-50": {
        "A1": NormEntry(4, 5, 6, 7, 9, 6.0, 1.6),
        "A2": NormEntry(5, 7, 8, 10, 12, 8.5, 2.0),
        "A3": NormEntry(5, 8, 10, 11, 14, 9.8, 2.5),
        "A4": NormEntry(6, 9, 11, 12, 15, 10.7, 2.7),
        "A5": NormEntry(7, 10, 12, 14, 15, 11.7, 2.6),
        "B1": NormEntry(3, 4, 5, 6, 8, 4.9, 1.6),
        "A6": NormEntry(5, 8, 10, 12, 14, 9.8, 2.8),
        "A7": NormEntry(5, 7, 10, 11, 14, 9.6, 2.8),
        "Reconhecimento Lista A": NormEntry(-3, 8, 12, 14, 15, 9.9, 5.6),
        "Escore Total": NormEntry(29, 40, 49, 53, 61, 46.7, 9.6),
        "Aprend. longo das Tentativas": NormEntry(5, 12, 17, 22, 27, 16.5, 7.3),
        "Velocidade de Esquecimento": NormEntry(
            0.71, 0.85, 1.00, 1.10, 1.38, 1.01, 0.34
        ),
        "Interferência Proativa": NormEntry(0.40, 0.67, 0.80, 1.00, 1.50, 0.86, 0.31),
        "Interferência Retroativa": NormEntry(0.54, 0.73, 0.86, 0.97, 1.13, 0.84, 0.18),
    },
    "51-60": {
        "A1": NormEntry(3, 5, 6, 7, 9, 6.0, 1.9),
        "A2": NormEntry(5, 6, 8, 10, 12, 8.2, 2.3),
        "A3": NormEntry(5, 8, 10, 11, 14, 9.6, 2.5),
        "A4": NormEntry(7, 9, 11, 12, 14, 10.6, 2.4),
        "A5": NormEntry(8, 10, 12, 13, 15, 11.3, 2.3),
        "B1": NormEntry(2, 4, 5, 6, 8, 4.8, 1.7),
        "A6": NormEntry(5, 7, 10, 12, 14, 9.4, 3.1),
        "A7": NormEntry(4, 8, 10, 12, 14, 9.5, 3.2),
        "Reconhecimento Lista A": NormEntry(-2, 10, 13, 14, 15, 10.9, 5.2),
        "Escore Total": NormEntry(31, 37, 47, 53, 61, 45.7, 9.7),
        "Aprend. longo das Tentativas": NormEntry(4, 12, 15, 19, 26, 15.6, 7.4),
        "Velocidade de Esquecimento": NormEntry(
            0.80, 0.90, 1.00, 1.11, 1.38, 1.02, 0.19
        ),
        "Interferência Proativa": NormEntry(0.40, 0.63, 0.80, 1.00, 1.40, 0.82, 0.29),
        "Interferência Retroativa": NormEntry(0.45, 0.67, 0.84, 1.00, 1.08, 0.82, 0.19),
    },
    "61-70": {
        "A1": NormEntry(3, 5, 5, 6, 8, 5.5, 1.6),
        "A2": NormEntry(5, 6, 8, 9, 11, 7.8, 1.9),
        "A3": NormEntry(6, 8, 9, 10, 12, 9.1, 2.0),
        "A4": NormEntry(7, 9, 10, 12, 13, 10.3, 1.9),
        "A5": NormEntry(8, 10, 11, 13, 14, 11.3, 2.0),
        "B1": NormEntry(2, 4, 5, 5, 7, 4.7, 1.4),
        "A6": NormEntry(4, 8, 10, 11, 13, 9.5, 2.6),
        "A7": NormEntry(5, 8, 10, 11, 14, 9.4, 2.6),
        "Reconhecimento Lista A": NormEntry(3, 9, 11, 13, 15, 10.4, 3.8),
        "Escore Total": NormEntry(30, 40, 44, 49, 58, 44.0, 7.6),
        "Aprend. longo das Tentativas": NormEntry(6, 13, 17, 20, 27, 16.4, 6.1),
        "Velocidade de Esquecimento": NormEntry(
            0.78, 0.90, 1.00, 1.10, 1.38, 1.01, 0.24
        ),
        "Interferência Proativa": NormEntry(0.50, 0.67, 0.83, 1.00, 1.40, 0.92, 0.61),
        "Interferência Retroativa": NormEntry(0.55, 0.74, 0.86, 0.93, 1.04, 0.84, 0.16),
    },
    "71-79": {
        "A1": NormEntry(3, 4, 5, 6, 8, 5.09, 1.46),
        "A2": NormEntry(5, 6, 7, 8, 10, 6.96, 1.74),
        "A3": NormEntry(5, 7, 8, 9, 11, 7.98, 1.99),
        "A4": NormEntry(5, 8, 9, 11, 13, 9.19, 2.30),
        "A5": NormEntry(7, 9, 10, 12, 14, 10.27, 2.16),
        "B1": NormEntry(1, 3, 4, 5, 7, 4.05, 1.75),
        "A6": NormEntry(3, 7, 8, 10, 12, 8.29, 2.37),
        "A7": NormEntry(4, 7, 8, 9, 12, 8.05, 2.39),
        "Reconhecimento Lista A": NormEntry(1, 6, 7, 10, 14, 7.72, 3.99),
        "Escore Total": NormEntry(25, 35, 39, 44, 55, 39.48, 8.23),
        "Aprend. longo das Tentativas": NormEntry(4, 10, 14, 18, 24, 14.04, 5.70),
        "Velocidade de Esquecimento": NormEntry(
            0.25, 0.60, 0.80, 1.00, 1.75, 0.84, 0.39
        ),
        "Interferência Proativa": NormEntry(0.46, 0.73, 0.80, 0.91, 1.11, 0.81, 0.19),
        "Interferência Retroativa": NormEntry(0.73, 0.88, 1.00, 1.11, 1.50, 1.00, 0.29),
    },
    "80+": {
        "A1": NormEntry(2, 3, 4, 5, 6, 4.1, 1.4),
        "A2": NormEntry(4, 5, 6, 7, 9, 6.0, 1.5),
        "A3": NormEntry(5, 6, 7, 7, 10, 6.9, 1.7),
        "A4": NormEntry(6, 7, 8, 9, 11, 7.9, 1.6),
        "A5": NormEntry(7, 8, 10, 11, 13, 9.6, 2.1),
        "B1": NormEntry(0, 2, 3, 4, 6, 3.2, 1.7),
        "A6": NormEntry(4, 6, 8, 9, 11, 7.5, 2.2),
        "A7": NormEntry(4, 6, 7, 8, 10, 6.7, 2.0),
        "Reconhecimento Lista A": NormEntry(-2, 3, 6, 9, 14, 5.8, 5.4),
        "Escore Total": NormEntry(24, 31, 34, 36, 47, 34.5, 6.3),
        "Aprend. longo das Tentativas": NormEntry(5, 11, 13, 17, 22, 13.9, 5.5),
        "Velocidade de Esquecimento": NormEntry(
            0.64, 0.75, 0.89, 1.00, 1.20, 0.91, 0.23
        ),
        "Interferência Proativa": NormEntry(0.00, 0.57, 0.80, 1.00, 1.50, 0.81, 0.41),
        "Interferência Retroativa": NormEntry(0.45, 0.67, 0.78, 0.89, 1.13, 0.79, 0.22),
    },
}


AGE_BANDS = [
    (6, 8, "6-8"),
    (9, 11, "9-11"),
    (12, 14, "12-14"),
    (15, 17, "15-17"),
    (18, 20, "18-20"),
    (21, 30, "21-30"),
    (31, 40, "31-40"),
    (41, 50, "41-50"),
    (51, 60, "51-60"),
    (61, 70, "61-70"),
    (71, 79, "71-79"),
    (80, 200, "80+"),
]


def get_age_band(age: int) -> str:
    for start, end, label in AGE_BANDS:
        if start <= age <= end:
            return label
    raise ValueError("Idade fora da faixa normativa disponível.")


def safe_div(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b


def compute_recognition_score(correct_answers_out_of_50: int) -> int:
    return correct_answers_out_of_50 - 35


def z_score(raw: Optional[float], mean: float, sd: float) -> Optional[float]:
    if raw is None or sd == 0:
        return None
    return (raw - mean) / sd


def calc_weighted_score(z: Optional[float]) -> Optional[float]:
    if z is None:
        return None
    return 10 + (3 * z)


def percentile_from_z(z: Optional[float]) -> Optional[float]:
    if z is None:
        return None
    import math

    return 100 * (0.5 * (1 + math.erf(z / math.sqrt(2))))


def classify_by_percentile(percentile: Optional[float]) -> str:
    if percentile is None:
        return "-"

    p = round(percentile)

    if p >= 98:
        return "Muito Superior"
    if 91 <= p <= 97:
        return "Superior"
    if 75 <= p <= 90:
        return "Média Superior"
    if 25 <= p <= 74:
        return "Média"
    if 9 <= p <= 24:
        return "Média Inferior"
    if 2 <= p <= 8:
        return "Inferior"
    return "Muito Inferior"
