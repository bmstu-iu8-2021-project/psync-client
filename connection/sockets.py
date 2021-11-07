from socketIO_client import SocketIO
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal

from data_processing.constants import PROTOCOL, IP, PORT


def event_handler(function):
    def wrapper(*arg):
        return Thread(name=function.__name__, target=function, args=(*arg,)).start()

    return wrapper


class Socket(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, login):
        super().__init__()
        self.__socketIO = SocketIO(f'{PROTOCOL}://{IP}:{PORT}')
        self.__socketIO.on('message', self.message)
        self.__login = login
        self.join_flag = True

    @event_handler
    def join_room(self):
        self.__socketIO.emit('join_room', {'current_user': self.__login, 'room': 'users'})
        while self.join_flag:
            self.__socketIO.wait(seconds=1)

    def message(self, args):
        if type(args) is dict:
            if args['other_user'] != self.__login:
                return
            print(args)
            self.signal.emit(args)

    def send_answer(self, args):
        self.__socketIO.emit('send_answer',
                             {'current_user': args['current_user'], 'other_user': args['other_user'],
                              'choice': args['choice'], 'room': 'users'})

    def leave_room(self):
        self.join_flag = False
        self.__socketIO.emit('leave_room', {'current_user': self.__login, 'room': 'users'})
