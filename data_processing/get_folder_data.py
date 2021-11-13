import os
import uuid
from sys import platform


def get_mac():
    mac_adr = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_adr[i:i + 2] for i in range(0, 11, 2))
    return platform + '_' + mac


def get_files(path_name):
    files_list = []
    for root, dirs, files in os.walk(path_name):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list


def get_json(files):
    table = {
        'files': []
    }
    for file in files:
        table['files'].append({
            'name': file[file.find(':') + 1:].replace('\\', '/'),
            'timestamp': round(os.stat(file).st_mtime, 0)
        })
    return table
