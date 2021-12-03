import re

from UI.call_ui import show_dialog


def is_login_valid(login):
    if len(login) > 20:
        return False, 'The login is to long (more than 20)'
    if login.isdigit():
        return False, 'Login can`t consist only of numbers'
    alphabet = '0123456789qwertyuiopasdfghjklzxcvbnm_-.'
    for sym in login.lower():
        if sym not in alphabet:
            return False, 'Login cannot contain this symbol: %s' % sym
    return True, ''


def is_password_valid(password):
    if 7 < len(password) < 41:
        res = [
            re.search(r"[a-z]", password),
            re.search(r"[A-Z]", password),
            re.search(r"[0-9]", password),
            re.search(r"\W", password)
        ]
        if all(res):
            return True, ''
        return False, 'The password is too weak'
    return False, 'The password must be\nlonger than 8 characters'


def is_version_valid(version):
    if len(version) > 20:
        return False, 'The version name is to long (more than 20)'
    alphabet = '0123456789qwertyuiopasdfghjklzxcvbnm_-.+, '
    for sym in version.lower():
        if sym not in alphabet:
            return False, 'Version name cannot contain this symbol: %s' % sym
    return True, ''


def check_request(req):
    if req.ok:
        return True
    code = req.status_code
    if code == 400:
        show_dialog('Error!', 'The operation failed. Bad request or token was not found', 1)
    elif code == 403:
        show_dialog('Error!', 'The operation failed. Token was incorrect', 1)
    elif code == 404:
        show_dialog('Error!', 'Handler for this request was not found', 1)
    else:
        show_dialog('Error!', f'Unexpected error with code {code}', 1)
    return False
