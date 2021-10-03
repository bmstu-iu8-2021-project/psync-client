import re


def is_login_valid(login):
    alphabet = '0123456789qwertyuiopasdfghjklzxcvbnm_-.'
    if len(login) > 20:
        return False, 'The login is to long (more than 20)'
    if login.isdigit():
        return False, 'Login can`t consist only of numbers'
    else:
        for let in login.lower():
            if let not in alphabet:
                return False, 'Login cannot contain this symbol: %s' % let
    return True, ''


def is_mail_valid(mail):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'
    if not re.match(pattern, mail):
        return False, 'Mail seams to be incorrect'
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
    else:
        return False, 'The password must be \n8-40 characters long'
