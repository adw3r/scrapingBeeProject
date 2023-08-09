import json
import pathlib
from random import choice
from string import digits, ascii_letters

import config


def generate_text(length: int = 6, sequence=ascii_letters + digits) -> str:
    return ''.join([choice(sequence) for _ in range(length)])


def get_apikeys() -> list[str]:
    with open(config.APIKEY_PATH, 'r') as file:
        return json.load(file)


def dump_json(data: dict, file_name) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file)


def load_json(file_name: str | pathlib.Path) -> dict | list:
    with open(file_name, 'rb') as file:
        return json.load(file)
