from socketIO_client import SocketIO
from threading import Thread, enumerate

from data_processing.constants import PROTOCOL, IP, PORT
from UI.call_ui import show_warning

users = []


def join_room(login):
    Thread(name='join', target=thread_join_room, args=(login,)).start()


def thread_join_room(login):
    socketIO.emit('join_room', {'username': login, 'room': 'users'})
    socketIO.wait(seconds=1)


def leave_room(login):
    Thread(name='leave', target=thread_leave_room, args=(login,)).start()


def thread_leave_room(login):
    print(users)
    socketIO.emit('leave_room', {'username': login, 'room': 'users'})
    socketIO.wait(seconds=1)


def event_handler(function):
    def wrapper(arg):
        return Thread(name='print', target=function, args=(arg,)).start()
    return wrapper


@event_handler
def thread_on_message(args):
    if type(args) is dict:
        users.append(args['data'])
        print(args['data'])
        print(enumerate())
    # print(args)


socketIO = SocketIO(f'{PROTOCOL}://{IP}:{PORT}')
socketIO.on('message', thread_on_message)
