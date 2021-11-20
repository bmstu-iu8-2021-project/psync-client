import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from data_processing.get_folder_data import get_mac


def auth(login, password):
    try:
        request = requests.get(
            f'{PROTOCOL}://{IP}:{PORT}/auth/',
            params={
                'login': login,
                'password': password,
                'mac': get_mac()
            })
        if check_request(request):
            return request.content
    except requests.ConnectionError:
        return None
