from os import getenv

api_uri = 'https://uvercom.okdesk.ru/api/v1'
api_token = getenv('OKDESK_API_TOKEN')
token = {'api_token': api_token}
