import json

import requests

from settings import api_uri, token


def create_issue(title: str, **kwargs) -> int:
    '''Создание заявки'''
    payload = {
        'title': title
    }
    payload.update(kwargs)
    r = requests.post(f'{api_uri}/issues', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            issue_id = decoded_r['id']
            print(f"[ OK ] Заявка {issue_id} - создана")
            return issue_id
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def change_assignee(issue_id: int, assignee_id=None, group_id=None) -> None:
    '''Смена ответственного за заявку'''
    payload = {
        'assignee_id': assignee_id,
        'group_id': group_id
    }
    r = requests.patch(f'{api_uri}/issues/{issue_id}/assignees', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            if not decoded_r['assignee']:
                print(f"[ OK ] Заявка {issue_id} - снят ответственный")
            else:
                assignee_name = decoded_r['assignee']['name']
                print(f"[ OK ] Заявка {issue_id} - назначен ответственный: {assignee_name}")
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def change_issue_status(issue_id: int, status_code: str, **kwargs) -> None:
    '''Смена ответственного за заявку'''
    payload = {'code': status_code}
    payload.update(kwargs)
    r = requests.post(f'{api_uri}/issues/{issue_id}/statuses', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            issue_status = decoded_r['status']['name']
            print(f"[ OK ] Заявка {issue_id} - статус изменён на {issue_status}")
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def add_comment(issue_id: int, content: str, author_id: int, public=False, **kwargs) -> None:
    '''# Добавление комментария к заявке'''
    payload = {
        'content': content,
        'author_id': author_id,
        'public': public
    }
    payload.update(kwargs)
    r = requests.post(f'{api_uri}/issues/{issue_id}/comments', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            print(f"[ OK ] Заявки {issue_id} - добавлен комментарий")
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def get_issue_comments(issue_id: int) -> list:
    '''Получение списка комментариев заявки'''
    payload = {'issue_id': issue_id}
    r = requests.get(f'{api_uri}/issues/{issue_id}/comments', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            comment_list = decoded_r
            return comment_list
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def get_issue_list(**kwargs) -> list:
    '''Получение списка заявок по параметрам'''
    payload = kwargs
    payload.update(token)
    r = requests.get(f'{api_uri}/issues/count', params=payload)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            issue_list = decoded_r
            return issue_list
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def get_issue_services(issue_id: int) -> list:
    '''Получение спецификаций заявки'''
    r = requests.get(f'{api_uri}/issues/{issue_id}/services', params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            services = decoded_r
            return services
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def add_service(issue_id: int, code: str, quantity: float, **kwargs):
    '''Добавление спецификации к заявке'''
    payload = {
        'issue_service': {
            'code': str(code),
            'quantity': quantity,
        }
    }
    payload.update(kwargs)
    r = requests.post(f'{api_uri}/issues/{issue_id}/services', json=payload, params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            print(f"[ OK ] Заявка {issue_id} - добавлена спецификация")
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def get_issue_info(issue_id: int) -> dict:
    '''Информация о заявке'''
    r = requests.get(f'{api_uri}/issues/{issue_id}', params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            issue_info_dict = decoded_r
            return issue_info_dict
        else:
            print(f"[ ERROR ] {decoded_r['errors']}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()


def delete_issue(issue_id: int) -> None:
    '''Удаление заявки'''
    r = requests.delete(f'{api_uri}/issues/{issue_id}', params=token)
    try:
        decoded_r = json.loads(r.text)
        if 'errors' not in decoded_r:
            result = decoded_r['result']
            issue_id = decoded_r['issue']['id']
            print(f"[ OK ] Заявка {issue_id} - {result.lower()}")
    except json.decoder.JSONDecodeError:
        r.raise_for_status()
