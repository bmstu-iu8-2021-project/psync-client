import requests

from data_processing.get_folder_data import get_mac
from data_processing.data_validation import check_request
from data_processing.constants import PROTOCOL, IP, PORT


def terminate_sync(current_login, other_id, current_folder, other_folder, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/terminate_sync/',
        params={
            'current_login': current_login,
            'other_id': other_id,
            'current_folder': current_folder,
            'other_folder': other_folder,
            'current_mac': get_mac(),
        },
        headers=head
    )
    return check_request(request)


def synchronize_folder(sender_login, sender_folder, receiver_id, receiver_folder, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/synchronize_folder/',
        params={
            'sender_login': sender_login,
            'sender_mac': get_mac(),
            'sender_folder': sender_folder,
            'receiver_id': receiver_id,
            'receiver_folder': receiver_folder,
        },
        headers=head
    )
    return check_request(request)
