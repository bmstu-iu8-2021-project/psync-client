import shutil
import threading
import time
import requests
import os
from os.path import join
import zipfile
import json
import bcrypt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog

from data_processing.get_folder_data import get_mac, get_json, get_files
from data_processing.constants import PROTOCOL, IP, PORT
from data_processing.data_validation import check_request
from UI.call_ui import show_dialog


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
        return request.json()
    return None


def check_actuality(login, json_data, token):
    if json_data is not None:
        to_check = {'login': login, 'mac': get_mac(), 'folder': []}
        json_data = [item for item in json_data if item['is_actual']]
        for item in json_data:
            to_check_item = {
                'name': item['folder'].replace('\\', '/'),
                'files': get_json(get_files(item['folder']))['files']
            }
            to_check['folder'].append(to_check_item)

        if len(to_check['folder']) > 0:
            head = {'Content-Type': 'application/json', 'Authorization': token}
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/check_actuality/',
                data=json.dumps(to_check),
                headers=head
            )
            if check_request(request):
                to_change = request.json()
                if len(to_change['folder']):
                    return to_change
    return None


def make_no_actual(login, path, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/make_no_actual/',
        params={
            'login': login,
            'mac': get_mac(),
            'path': path,
        },
        headers=head
    )
    return check_request(request)


def update_actual_folder(login, path, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/get_actual_version/',
        params={
            'login': login,
            'mac': get_mac(),
            'path': path
        },
        headers=head
    )
    if check_request(request):
        version = request.content.decode('UTF-8')
        return update_version(
            login=login,
            path=path,
            version=version,
            token=token
        )
    return False


def check_synchronized(login, token):
    head = {'Content-Type': 'application/json', 'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/check_synchronized/',
        params={
            'login': login,
            'mac': get_mac()
        },
        headers=head
    )
    if check_request(request):
        return request.json()
    return None


def add_version(login, path, version, token):
    mac = get_mac()
    folder_content = get_json(get_files(path))
    folder_content['login'] = login
    folder_content['mac'] = mac
    folder_content['folder_path'] = path
    folder_content['version'] = version
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
            show_dialog('Conflict of versions!', 'Version with this name for this folder is already exist!')
        else:
            threading.Thread(name='upload_folder', target=upload_folder, kwargs={
                'login': login,
                'path': path,
                'version': version,
                'token': token
            }).start()
            # отправляем данные в бд
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/add_version/',
                data=json.dumps(folder_content),
                headers=head,
            )
            return check_request(request)
    return False


def upload_folder(login, path, version, token):
    # создаем архив
    zip_name = '_'.join([login, path[path.rfind('/') + 1:], version]) + '.zip'
    zip_folder = zipfile.ZipFile(zip_name, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_folder.write(join(root, file))
    zip_folder.close()

    # отправляем архив
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/upload_folder/',
        files={'file': (zip_name, open(zip_name, 'rb'))},
        headers={'Authorization': token},
    )

    if check_request(request):
        # удаляем архив
        os.remove(zip_name)


def delete_version(login, path, version, token):
    head = {'Authorization': token}
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


def update_version(login, path, version, token):
    threading.Thread(name='upload_folder', target=upload_folder, kwargs={
        'login': login,
        'path': path,
        'version': version,
        'token': token
    }).start()
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/update_version/',
        params={
            'login': login,
            'mac': get_mac(),
            'folder_path': path,
            'version': version
        },
        headers=head
    )
    return check_request(request)


def delete_user(login, token, window):
    count = 0
    head = {'Authorization': token}
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
                    request = requests.get(
                        f'{PROTOCOL}://{IP}:{PORT}/delete_user/',
                        params={'login': login},
                        headers=head
                    )
                    return check_request(request)
            else:
                break
        if count == 3:
            show_dialog('Confirmation error!', 'You have entered the wrong password too many times.')
    return False


# флаг равен 1, когда нужно актуальная версия, при этом имя версии не передаем
def download_version(login, path, token, version=None, flag=False):
    head = {'Authorization': token}
    if flag:
        request = requests.get(
            f'{PROTOCOL}://{IP}:{PORT}/get_actual_version/',
            params={
                'login': login,
                'mac': get_mac(),
                'path': path
            },
            headers=head
        )
        if check_request(request):
            version = request.content.decode('UTF-8')
        else:
            return
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/download_folder/',
        params={
            'login': login,
            'mac': get_mac(),
            'folder_path': path,
            'version': version,
        },
        headers=head
    )
    if check_request(request):
        if not os.path.exists(path):
            os.mkdir(path)
        for file in os.listdir(path):
            if os.path.isdir(join(path, file)):
                shutil.rmtree(join(path, file))
            else:
                os.remove(join(path, file))

        temp = str(time.time())
        archive_path = join(path, f'{temp}.zip')
        archive = open(archive_path, 'wb')
        archive.write(request.content)
        archive.close()

        arch_data = {}
        archive = zipfile.ZipFile(archive_path, 'r')
        for file in archive.namelist():
            arch_data[file] = time.mktime(tuple(list(archive.getinfo(file).date_time) + [0, 0, 0]))
        for file in archive.namelist():
            if os.path.basename(file):
                archive.extract(file, path[:path.find('/') + 1])
        archive.close()
        os.remove(archive_path)
        for root, dirs, files in os.walk(path):
            for file in files:
                path_file = join(root, file)
                os.utime(
                    path_file,
                    (arch_data[path_file[path_file.find('/') + 1:].replace('\\', '/')],
                     arch_data[path_file[path_file.find('/') + 1:].replace('\\', '/')])
                )


def synchronize(sender_login, sender_folder, receiver_login, token):
    head = {'Authorization': token}
    request = requests.get(
        f'{PROTOCOL}://{IP}:{PORT}/synchronize/',
        params={
            'sender_login': sender_login,
            'sender_folder': sender_folder,
            'sender_mac': get_mac(),
            'receiver_login': receiver_login,
            'room': 'users'
        },
        headers=head
    )
    if check_request(request):
        if request.content.decode('UTF-8') == 'False':
            show_dialog('Unable to connect', f'User {receiver_login} is offline, unable to send request')
        return


def make_actual(login, path, version, token):
    head = {'Authorization': token}
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
