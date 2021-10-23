import bcrypt
import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request, is_mail_valid
from UI.call_ui import show_warning


def change_mail(login, new_mail, password, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        params={
            'login': login
        },
        headers=head)
    if check_request(request):
        if bcrypt.checkpw(password.encode('UTF-8'), request.content):
            check = is_mail_valid(new_mail)
            if check[0]:
                head = {'Content-Type': 'application/json', 'Authorization': token}
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/change_mail/',
                    params={
                        'login': login,
                        'email': new_mail
                    },
                    headers=head)
                return check_request(request)
            else:
                show_warning('Wrong data!', check[1])
        else:
            show_warning('Wrong data!', 'You entered wrong password!')
    return False


def change_password():
    pass
