from socketIO_client import SocketIO
from threading import Thread, enumerate, current_thread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import queue

from data_processing.constants import PROTOCOL, IP, PORT
from UI.call_ui import AMessageBox, ThreadClass

# window = None
# join_flag, leave_flag = False, False
# username = ''
# socketIO = None
#
#
# def connect():
#     global socketIO
#     socketIO = SocketIO(f'{PROTOCOL}://{IP}:{PORT}')
#     socketIO.on('message', message)


def event_handler(function):
    def wrapper(*arg):
        return Thread(name=function.__name__, target=function, args=(*arg,)).start()
    return wrapper


# @event_handler
# def join_room(login, wpw):
#     global username
#     username = login
#     global window
#     window = wpw
#     socketIO.emit('join_room', {'username': login, 'room': 'users'})
#     while join_flag:
#         socketIO.wait(seconds=1)
#
#
# @event_handler
# def leave_room(login):
#     socketIO.emit('leave_room', {'username': login, 'room': 'users'})
#     while leave_flag:
#         socketIO.wait(seconds=1)


# @event_handler
# def message(args):
#     print('here')
#     if type(args) is dict:
#         if args['type'] == 'request_to_synchronize':
#             if args['receiver'] != 'dmitrii':
#                 return
#             # tc = ThreadClass()
#             # tc.start()
#             # tc.finish.connect(finish)
#
#             print(args)
#             # window.emit('got data')
#
#             # print(current_thread())
#             # print(enumerate())
#             # mb = AMessageBox('title', f"User {args['sender']} want to synchronize\n{args['folder']} with you")
#             # mb.start()
#
#             # accept_synchronize('Title',
#             #                    'User ' + args['sender'] + ' want to synchronize\n' + args['folder'] + ' with you')


# def finish():
#     mbox = QMessageBox()
#     mbox.exec_()


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
        print('j', current_thread())
        self.__socketIO.emit('join_room', {'username': self.__login, 'room': 'users'})
        while self.join_flag:
            self.__socketIO.wait(seconds=1)

    def message(self, args):
        if type(args) is dict:
            if args['type'] == 'request_to_synchronize':
                if args['receiver'] != self.__login:
                    return
                self.signal.emit(args)

    def leave_room(self):
        print('l', current_thread())
        self.join_flag = False
        self.__socketIO.emit('leave_room', {'username': self.__login, 'room': 'users'})
    #
    # def __del__(self):
    #     self.join_flag = False
    #     self.leave_room()
