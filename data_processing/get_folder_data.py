import os
import uuid
from sys import platform


def get_mac():
    mac_adr = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_adr[i:i + 2] for i in range(0, 11, 2))
    return platform + '_' + mac


def get_files(path_file):
    fls = []
    for file in os.listdir(path_file):
        if os.path.isfile(path_file + '/' + file):
            fls.append(path_file + '/' + file)
        elif os.path.isdir(path_file + '/' + file):
            fls += get_files(path_file + '/' + file)
    return fls


def get_json(fls):
    table = {
        'login': '',
        'mac': '',
        'path_file': '',
        'old_version': '',
        'new_version': '',
        'files': dict()
    }
    for file in fls:
        table['files'][file] = os.stat(file).st_mtime
    return table
