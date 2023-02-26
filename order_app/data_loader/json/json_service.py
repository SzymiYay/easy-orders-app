from typing import Any
import json


def load_from_json(filename: str) -> list[dict[str, Any]]:
    with open(filename, 'r') as jf:
        return json.load(jf)


def save_to_json(filename: str, data: dict[str, Any]) -> None:
    with open(filename, 'w') as jf:
        json.dump(data, jf, indent=4)
