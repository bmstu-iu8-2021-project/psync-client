import requests

from data_processing.get_folder_data import get_mac
from data_processing.data_validation import check_request
from data_processing.constants import PROTOCOL, IP, PORT


def get_synchronized(login, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_synchronized/',
        params={
            'login': login,
            'mac': get_mac()
        },
        headers=head
    )
    if check_request(request):
        return request.json()
    return None
