import sqlite3


def create():
    conn = sqlite3.connect('databases//users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            login varchar(20),
            mail varchar(30),
            password varchar(40),
            PRIMARY KEY (login)
        );
    ''')
    conn.commit()
    return conn


def check(conn, reg_data):
    er_mes = 'This login is already taken.'
    if not find_record(conn, reg_data[0], mode=0):
        er_mes = 'This mail is already taken.'
        if not find_record(conn, reg_data[1], mode=1):
            return True, ''
    return False, er_mes


def get_password(conn, login):
    cr = conn.cursor()
    cr.execute('SELECT password FROM user WHERE login = ?;', tuple([login]))
    password = cr.fetchall()
    return password[0][0]


def add_user(conn, data):
    cr = conn.cursor()
    cr.execute('INSERT INTO user VALUES(?, ?, ?);', data)
    conn.commit()


def access_request(conn, login, password):
    cr = conn.cursor()
    cr.execute('SELECT password FROM user WHERE login = ?;', tuple([login]))
    data = cr.fetchall()
    if data:
        data = data[0][0]
        if data == password:
            return True
    return False


def delete_user(conn, login):
    cr = conn.cursor()
    cr.execute('DELETE FROM user WHERE login = ?;', tuple([login]))
    conn.commit()


def find_record(conn, data, mode=0):
    if mode < 3:
        cr = conn.cursor()
        if mode == 0:  # login
            cr.execute('SELECT * FROM user WHERE login = ?;', tuple([data]))
            read = cr.fetchall()
            if read:
                return True
        elif mode == 1:  # mail
            cr.execute('SELECT * FROM user WHERE mail = ?;', tuple([data]))
            read = cr.fetchall()
            if read:
                return True
        else:  # password
            cr.execute('SELECT * FROM user WHERE password = ?;', tuple([data]))
            read = cr.fetchall()
            if read:
                return True
    return False


def change_mail(conn, login, mail):
    cr = conn.cursor()
    cr.execute('UPDATE user SET mail = ? WHERE login = ?;', tuple([mail, login]))
    conn.commit()


def change_password(conn, login, password):
    cr = conn.cursor()
    cr.execute('UPDATE user SET password = ? WHERE login = ?;', tuple([password, login]))
    conn.commit()


def show(conn):
    cr = conn.cursor()
    cr.execute('SELECT * FROM user')
    table = cr.fetchall()
    for record in table:
        print(record)


def close(conn):
    conn.close()
