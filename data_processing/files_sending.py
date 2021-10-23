import requests
import json
from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from UI import call_ui


def send_folder(data, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    # проверка, сохранены есть ли уже сохранение этой папки с этим названием версии
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/find_version/',
        params={
            'login': data['login'],
            'mac': data['mac'],
            'folder_path': data['path_file'],
            'version': data['new_version']
        },
        headers=head
    )

    if check_request(request):
        if request.content.decode('UTF-8') == '1':
            call_ui.show_warning('Conflict of versions!',
                                 'Version with this name for this folder is already exist!')
    if True:
        if False:
            pass
        else:
            # отправляем данные
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/add_version/',
                data=json.dumps(data),
                headers=head
            )
            if check_request(request):
                self.fill_table()