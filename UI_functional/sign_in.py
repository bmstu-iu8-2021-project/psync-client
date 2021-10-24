import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request


def auth(login, password):
    request = requests.get(f'{PROTOCOL}://{IP}:{PORT}/auth/',
                           params={
                               'login': login,
                               'password': password,
                           })
    if check_request(request):
        return request.content
    return None