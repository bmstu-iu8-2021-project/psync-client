import requests

from data_processing.get_folder_data import get_mac
from data_processing.data_validation import check_request
from data_processing.constants import PROTOCOL, IP, PORT


def terminate_sync(current_login, other_login, current_folder, other_folder, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/terminate_sync/',
        params={
            'current_login': current_login,
            'other_login': other_login,
            'current_folder': current_folder,
            'other_folder': other_folder,
            'current_mac': get_mac(),
        },
        headers=head
    )
    return check_request(request)


def synchronize_folder(current_login, current_folder, other_login, other_folder, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/synchronize_folder/',
        params={
            'current_login': current_login,
            'current_mac': get_mac(),
            'current_folder': current_folder,
            'other_login': other_login,
            'other_folder': other_folder,
        },
        headers=head
    )
    return check_request(request)
