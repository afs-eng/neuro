from apps.tests.wais3 import utils
from apps.tests.wais3.loaders import WAIS3NormLoader


def test_semelhancas_40_anos_raw_23_scaled_11():
    loader = WAIS3NormLoader()
    result = utils.convert_wais3_raw_to_scaled(age_years=40, age_months=0, subtest_key="semelhancas", raw_score=23, loader=loader)
    assert int(result) == 11

def test_semelhancas_40_anos_raw_31_scaled_14():
    loader = WAIS3NormLoader()
    result = utils.convert_wais3_raw_to_scaled(age_years=40, age_months=0, subtest_key="semelhancas", raw_score=31, loader=loader)
    assert int(result) == 14


def test_verbal_sum():
    scaled_scores = {
        "vocabulario": {"value": 11, "parenthetical": False, "included_in_primary_sum": True},
        "semelhancas": {"value": 13, "parenthetical": False, "included_in_primary_sum": True},
        "aritmetica": {"value": 8, "parenthetical": False, "included_in_primary_sum": True},
        "digitos": {"value": 7, "parenthetical": False, "included_in_primary_sum": True},
        "informacao": {"value": 13, "parenthetical": False, "included_in_primary_sum": True},
    }
    assert utils.sum_scaled_scores(scaled_scores, utils.WAIS3_DOMAINS["verbal"]) == 52


def test_parenthetical_values_are_not_included():
    scaled_scores = {
        "codigos": {"value": 10, "parenthetical": False, "included_in_primary_sum": True},
        "procurar_simbolos": {"value": 9, "parenthetical": True, "included_in_primary_sum": False},
    }
    assert utils.sum_scaled_scores(scaled_scores, utils.WAIS3_DOMAINS["ivp"]) == 10


def test_convert_qiv_sum_65_to_standard_score_105():
    # use existing CSVs via loader to read composite table
    loader = WAIS3NormLoader()
    rows = loader._read_csv_rows(loader.base_path / "composite_scores" / "qi_verbal.csv")
    # prepare sums
    sums = {"verbal": 65}
    conv_tables = {"composite_scores/qi_verbal.csv": rows}
    comps = utils.compute_wais3_composites(sums=sums, conversion_tables=conv_tables)
    qiv = comps.get("qi_verbal")
    assert qiv["standard_score"] == 105
    assert int(float(qiv["percentile"])) == 63
