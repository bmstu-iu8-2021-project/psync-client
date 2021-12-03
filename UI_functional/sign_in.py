import json
import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from data_processing.get_folder_data import get_mac
from UI.call_ui import show_dialog


def auth(login, password):
    try:
        request = requests.get(
            f'{PROTOCOL}://{IP}:{PORT}/auth/',
            params={
                'login': login,
                'password': password,
                'mac': get_mac()
            },
            headers={'Content-Type': 'application/json'}
        )
        if check_request(request):
            answer = request.json()
            if not answer['access']:
                show_dialog('Unable', 'You are already signed in.')
            else:
                if not answer['token']:
                    show_dialog('Wrong data!', 'The entered login or password is incorrect.')
                else:
                    answer.pop('access')
                    return json.dumps(answer)
        return None
    except requests.ConnectionError:
        show_dialog('Connection error!', 'Check your internet connection', 1)
        return None
