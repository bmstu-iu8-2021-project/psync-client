import requests
import os
import zipfile
import json
import bcrypt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog

from data_processing.get_folder_data import get_mac, get_json, get_files
from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from UI.call_ui import show_warning


def add_folder(login, path, version, token):
    mac = get_mac()
    folder_content = get_json(get_files(path))
    folder_content['login'] = login
    folder_content['mac'] = mac
    folder_content['path_file'] = path
    folder_content['new_version'] = version
    folder_content['is_actual'] = False

    head = {'Content-Type': 'application/json', 'Authorization': token}

    # проверка, сохранены есть ли уже сохранение этой папки с этим названием версии
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/find_version/',
        params={
            'login': login,
            'mac': mac,
            'folder_path': path,
            'version': version
        },
        headers=head
    )

    if check_request(request):
        if request.content.decode('UTF-8') == 'False':
            show_warning('Conflict of versions!',
                         'Version with this name for this folder is already exist!')
        else:
            # создаем архив
            zip_name = '_'.join([login, path[path.rfind('/') + 1:], version]) + '.zip'
            zip_folder = zipfile.ZipFile(zip_name, 'w')
            for root, dirs, files in os.walk(path):
                for file in files:
                    zip_folder.write(os.path.join(root, file))
            zip_folder.close()

            # отправляем архив
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/upload_folder/',
                files={
                    'file': (zip_name, open(zip_name, 'rb'))
                },
                headers={'Authorization': token},
            )

            if check_request(request):
                # удаляем архив
                os.remove(zip_name)

                # отправляем данные в бд
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/add_version/',
                    data=json.dumps(folder_content),
                    headers=head,
                )
                return check_request(request)
    return ''


def update_folder(login, path, old_version, new_version, token):
    data = get_json(get_files(path))
    data['login'] = login
    data['mac'] = get_mac()
    data['path_file'] = path
    data['old_version'] = old_version
    data['new_version'] = new_version

    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/update_version/',
        data=json.dumps(data),
        headers=head
    )
    return check_request(request)


def delete_version(login, path, version, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/delete_version/',
        params={
            'login': login,
            'mac': get_mac(),
            'folder_path': path,
            'version': version,
        },
        headers=head
    )
    return check_request(request)


def delete_user(login, token, window):
    count = 0
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        params={
            'login': login
        },
        headers=head)
    if check_request(request):
        password = request.content
        while count != 3:
            pass_input, flag = QInputDialog.getText(
                window,
                'Confirm your actions',
                'To delete your account, enter your password.',
                echo=QtWidgets.QLineEdit.Password
            )
            if flag and pass_input:
                count += 1
                if bcrypt.checkpw(pass_input.encode('UTF-8'), password):
                    head = {'Content-Type': 'application/json', 'Authorization': token}
                    request = requests.get(
                        f'{PROTOCOL}://{IP}:{PORT}/delete_user/',
                        params={
                            'login': login
                        },
                        headers=head
                    )
                    return check_request(request)
            else:
                break
        if count == 3:
            show_warning('Confirmation error!', 'You have entered the wrong password too many times.')
    return False


def get_folders(login, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    # получаем данные о папках этого пользователя, этого устройства
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_folders/',
        params={
            'login': login,
            'mac': get_mac(),
        },
        headers=head
    )
    if check_request(request):
        return json.loads(request.content.decode('UTF-8'))
    return None


def make_actual(login, path, version, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/make_actual/',
        params={
            'login': login,
            'mac': get_mac(),
            'path': path,
            'version': version
        },
        headers=head
    )
    return check_request(request)


def check_actuality(login, data, token):
    if data.keys():
        to_check = {'zip_name': [], 'content': []}
        for row in range(len(data['is_actual'])):
            if data['is_actual'][row] == 'True':
                path = data['folder'][row]
                version = data['version'][row]
                to_check['zip_name'].append('_'.join([login, path[path.rfind('/') + 1:], version]) + '.zip')
                to_check['content'].append(get_json(get_files(data['folder'][row]))['files'])
        output = json.dumps(to_check)

        head = {'Content-Type': 'application/json', 'Authorization': token}
        request = requests.get(
            f'{PROTOCOL}://{IP}:{PORT}/check_actuality/',
            data=output,
            headers=head
        )
        if check_request(request):
            print(json.loads(request.content.decode('UTF-8')))


def check_actual(login, data, token):
    pass
