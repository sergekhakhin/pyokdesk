import json

import requests

from settings import api_uri, token


def search_company_id(search_string: str) -> int:
    payload = {'search_string': search_string}
    r = requests.get(f'{api_uri}/companies', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if decoded_r:
            company_id = decoded_r[0]['id']
            return company_id
        else:
            print(f"[ ERROR ] Не удалось найти компанию")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def get_company_info_by_id(company_id: int):
    payload = {'id': company_id}
    r = requests.get(f'{api_uri}/companies', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if decoded_r:
            company_info_dict = decoded_r
            return company_info_dict
        else:
            print(f"[ ERROR ] Не удалось найти компанию с заданным ID")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()
