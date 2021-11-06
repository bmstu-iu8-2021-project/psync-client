from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from threading import current_thread, enumerate
import time


def show_warning(title, text, flag='Warning'):
    error = QMessageBox()
    error.setWindowTitle(title)
    error.setText(text)
    if flag == 'Warning':
        error.setIcon(QMessageBox.Warning)
    elif flag == 'Critical':
        error.setIcon(QMessageBox.Critical)
    error.setStandardButtons(QMessageBox.Ok)
    error.exec_()


# def accept_synchronize(title, text):
#     print(enumerate())
#     print(current_thread())
#     print(main_thread())
#     admitting = QMessageBox()
#     admitting.setWindowTitle(title)
#     admitting.setText(text)
#     admitting.setIcon(QMessageBox.Information)
#     admitting.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#     admitting.setDefaultButton(QMessageBox.Yes)
#     admitting.buttonClicked.connect(clicked)
#     admitting.exec_()


class AMessageBox(QThread):
    def __init__(self, title, text):
        QThread.__init__(self)
        self.__admitting = QMessageBox()
        self.__title = title
        self.__text = text
        print('\t', enumerate())
        print('\t', current_thread())

    def run(self):
        print(enumerate())
        print(current_thread())
        self.__admitting.setWindowTitle(self.__title)
        self.__admitting.setText(self.__text)
        self.__admitting.setIcon(QMessageBox.Information)
        self.__admitting.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.__admitting.setDefaultButton(QMessageBox.Yes)
        self.__admitting.buttonClicked.connect(clicked)
        self.__admitting.exec()
        # self.wait(100)

    # def __del__(self):
    #     print('stop')
    #     self.wait()


def clicked(button):
    print(button.text())


class ThreadClass(QThread):
    sig = pyqtSignal(int)
    finish = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        for t in range(5):
            self.sig.emit(t)
            QThread.msleep(1000)
        self.finish.emit()
