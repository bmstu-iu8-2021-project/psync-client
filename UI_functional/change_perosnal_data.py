import bcrypt
import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request, is_mail_valid, is_password_valid
from UI.call_ui import show_dialog


def change_mail(login, new_mail, password, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        params={
            'login': login
        },
        headers=head)
    if check_request(request):
        if not bcrypt.checkpw(password.encode('UTF-8'), request.content):
            show_dialog('Wrong data!', 'You entered wrong password!')
        else:
            check = is_mail_valid(new_mail)
            if not check[0]:
                show_dialog('Wrong data!', check[1])
            else:
                head = {'Content-Type': 'application/json', 'Authorization': token}
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/change_mail/',
                    params={
                        'login': login,
                        'email': new_mail
                    },
                    headers=head)
                return check_request(request)
    return False


def change_password(login, old_password, new_password, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        params={
            'login': login
        },
        headers=head)
    if check_request(request):
        if not bcrypt.checkpw(old_password.encode('UTF-8'), request.content):
            show_dialog('Wrong data!', 'You entered wrong password!')
        else:
            check = is_password_valid(new_password)
            if not check[0]:
                show_dialog('Wrong data!', check[1])
            else:
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/change_password/',
                    params={
                        'login': login,
                        'password': bcrypt.hashpw(new_password.encode('UTF-8'), bcrypt.gensalt(rounds=5))
                    },
                    headers=head)
                return check_request(request)
    return False
