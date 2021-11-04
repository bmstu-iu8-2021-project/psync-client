from socketIO_client import SocketIO
from threading import Thread

from data_processing.constants import PROTOCOL, IP, PORT

username = ''
socketIO = None
join_flag = True
leave_flag = True


def connect():
    global socketIO
    socketIO = SocketIO(f'{PROTOCOL}://{IP}:{PORT}')
    socketIO.on('message', message)


def join_room(login):
    global username
    username = login
    Thread(name='join', target=thread_join_room, args=(login,)).start()


def thread_join_room(login):
    socketIO.emit('join_room', {'username': login, 'room': 'users'})
    while join_flag:
        socketIO.wait(seconds=1)


def leave_room(login):
    Thread(name='leave', target=thread_leave_room, args=(login,)).start()


def thread_leave_room(login):
    socketIO.emit('leave_room', {'username': login, 'room': 'users'})
    while leave_flag:
        socketIO.wait(seconds=1)


def event_handler(function):
    def wrapper(arg):
        return Thread(name='event_handler', target=function, args=(arg,)).start()

    return wrapper


@event_handler
def message(args):
    if type(args) is dict:
        if args['type'] == 'request_to_synchronize':
            if args['receiver'] != username:
                return
            print(args['message'])
