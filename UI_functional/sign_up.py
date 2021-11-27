import requests
import bcrypt

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from data_processing.get_folder_data import get_mac
from UI.call_ui import show_dialog


def register(login, password):
    if login and password:
        if requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/find_login/',
                params={
                    'login': login
                }
        ).text == 'False':
            show_dialog('Wrong data!', 'This login seems to be taken.')
        else:
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/add_user/',
                params={
                    'login': login,
                    'mac': get_mac(),
                    'password': bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(rounds=5)),
                })
            if check_request(request):
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/auth/',
                    params={
                        'login': login,
                        'password': password,
                        'mac': get_mac()
                    })
                if check_request(request):
                    return request.content
    else:
        show_dialog('Wrong data!', 'Check the correctness of the data you entered.')
    return False
