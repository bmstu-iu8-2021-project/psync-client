from socketIO_client import SocketIO

from data_processing.constants import PROTOCOL, IP, PORT


def on_message(args):
    if type(args) is dict:
        print(args['data'])


def join_room(login):
    socketIO.emit('join_room', {'username': login, 'room': 'users'})
    socketIO.wait(seconds=1)


def leave_room(login):
    socketIO.emit('leave_room', {'username': login, 'room': 'users'})
    socketIO.wait(seconds=1)


socketIO = SocketIO(f'{PROTOCOL}://{IP}:{PORT}')
socketIO.on('message', on_message)
