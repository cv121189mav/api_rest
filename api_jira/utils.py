import requests

DOMAIN = 'http://127.0.0.1:8080'


def send_request(url, method="GET", data=None, permission=''):
    if method == "GET":
        return requests.get(f'{DOMAIN}{url}')

    if method == "POST":
        return requests.post(f'{DOMAIN}{url}', data=data)
    if method == "DELETE":
        return requests.delete(f'{DOMAIN}{url}', data=data)

    if method == "PATCH":
        return requests.patch(f'{DOMAIN}{url}', data=data)