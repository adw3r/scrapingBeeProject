import json
import pathlib
from random import choice
from string import digits, ascii_letters

import bs4
import requests

from app import config


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


def check_form(url):
    cookies = {
        '_ga': 'GA1.2.722049793.1693989861',
        '_gid': 'GA1.2.1143209261.1693989861',
        '_gat': '1',
        '_ga_R1XPVJRD27': 'GS1.2.1693989861.1.1.1693989861.0.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        form = soup.find('form')
        if form:
            inputs = form.find_all('input')
            input_names = [i.get('name') for i in inputs]
    except Exception as error:
        print(error)
