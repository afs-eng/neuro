def find_strengths_weaknesses(
    subtest_results: list[dict],
) -> tuple[list[str], list[str]]:
    if not subtest_results:
        return [], []

    percentis = [
        (r["subteste"], r["percentil"]) for r in subtest_results if r["codigo"] != "ag"
    ]
    if not percentis:
        return [], []

    media = sum(p for _, p in percentis) / len(percentis)

    strengths = [name for name, perc in percentis if perc > media + 20]
    weaknesses = [name for name, perc in percentis if perc < media - 20]

    return strengths, weaknesses
