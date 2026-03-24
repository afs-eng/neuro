from .config import WISC4_INDICES, IndexCode


SIGNIFICANT_DIFFERENCE_THRESHOLDS = {
    "subtest_vs_index": 3,
    "index_vs_index": 15,
    "index_vs_qi": 15,
}


def find_strengths_weaknesses(
    subtest_results: list[dict],
) -> tuple[list[str], list[str]]:
    if not subtest_results:
        return [], []

    scores = [(r["subteste"], r["escore_padrao"]) for r in subtest_results]
    media = sum(s for _, s in scores) / len(scores)

    strengths = [name for name, score in scores if score > media + 3]
    weaknesses = [name for name, score in scores if score < media - 3]

    return strengths, weaknesses


def find_significant_differences(
    indices: list[dict],
    qi_total: int,
) -> list[str]:
    differences = []

    for i, idx1 in enumerate(indices):
        for idx2 in indices[i + 1 :]:
            diff = abs(idx1["escore_composto"] - idx2["escore_composto"])
            if diff >= SIGNIFICANT_DIFFERENCE_THRESHOLDS["index_vs_index"]:
                differences.append(
                    f"Diferença significativa entre {idx1['nome']} e {idx2['nome']}: {diff} pontos"
                )

    for idx in indices:
        diff = abs(idx["escore_composto"] - qi_total)
        if diff >= SIGNIFICANT_DIFFERENCE_THRESHOLDS["index_vs_qi"]:
            differences.append(
                f"{idx['nome']} difere significativamente do QI Total: {diff} pontos"
            )

    return differences
