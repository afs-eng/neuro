from pathlib import Path
from pprint import pprint

from apps.tests.bai import BAIModule


if __name__ == "__main__":
    module = BAIModule(chart_output_dir=Path("./_charts"))
    raw_payload = {
        "respondent_name": "Juliana",
        "application_mode": "paper",
        "responses": [
            {"item_number": 1, "score": 0},
            {"item_number": 2, "score": 2},
            {"item_number": 3, "score": 3},
            {"item_number": 4, "score": 3},
            {"item_number": 5, "score": 3},
            {"item_number": 6, "score": 1},
            {"item_number": 7, "score": 2},
            {"item_number": 8, "score": 1},
            {"item_number": 9, "score": 1},
            {"item_number": 10, "score": 3},
            {"item_number": 11, "score": 1},
            {"item_number": 12, "score": 1},
            {"item_number": 13, "score": 2},
            {"item_number": 14, "score": 3},
            {"item_number": 15, "score": 2},
            {"item_number": 16, "score": 2},
            {"item_number": 17, "score": 1},
            {"item_number": 18, "score": 0},
            {"item_number": 19, "score": 1},
            {"item_number": 20, "score": 1},
            {"item_number": 21, "score": 2},
        ],
    }
    result = module.run(raw_payload)
    pprint(result)
    print("\nGráficos gerados em:", result["charts"])
