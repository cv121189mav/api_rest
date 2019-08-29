import requests

DOMAIN = 'http://127.0.0.1:8080'


def send_request(url, method="GET", data=None, params=None):
    return requests.request(method, DOMAIN + url, params=params, data=data)
