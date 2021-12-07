import bcrypt
import requests

from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request, is_password_valid
from UI.call_ui import show_dialog


def change_password(login, old_password, new_password, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        params={'login': login},
        headers=head
    )
    if check_request(request):
        if not bcrypt.checkpw(old_password.encode('UTF-8'), request.content):
            show_dialog('Wrong data!', 'You entered wrong password!')
        else:
            check = is_password_valid(new_password)
            if not check[0]:
                show_dialog('Wrong data!', check[1])
            else:
                if old_password != new_password:
                    request = requests.get(
                        f'{PROTOCOL}://{IP}:{PORT}/change_password/',
                        params={
                            'login': login,
                            'new_password': bcrypt.hashpw(new_password.encode('UTF-8'), bcrypt.gensalt(rounds=5))
                        },
                        headers=head)
                    return check_request(request)
                else:
                    show_dialog('Wrong data!', 'Your new password can`t be the same as current')
    return False
