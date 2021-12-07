import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow

from UI_functional.synchronized import synchronize_folder
from UI_functional.workplace import download_version
from data_processing.get_folder_data import get_mac


class ASWindow(QMainWindow):
    def __init__(self, data, wpw):
        super(ASWindow, self).__init__()
        self.__data = data
        self.__wpw = wpw
        self.__socket = self.__wpw.socket
        self.__flag = True

        self.__wpw.setEnabled(False)

        self.setWindowTitle('SyncGad • Accepting')
        self.setGeometry(400, 400, 400, 313)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(12)

        self.desc_Label = QtWidgets.QLabel(self)
        self.desc_Label.setGeometry(10, 3, 390, 230)
        self.desc_Label.setFont(font)
        self.desc_Label.setText(f"<h4 style='text-align: justify;'>User <span style='color: #999999;'>"
                                f"<em>{self.__data['sender_login']}</em></span> want to<br> synchronize his local "
                                f"folder<br> <span style='color: #999999;'><em>{self.__data['sender_folder']}"
                                f"</em></span><br> with you.</h4><p style='text-align: justify;'>To accept the request, "
                                f"select the appropriate folder<br> from the list of relevant ones below. Now and in"
                                f"<br> the future, during authorization, the contents of<br> your folder will be "
                                f"automatically updated according<br> to the contents of the user`s folder <strong>"
                                f"{self.__data['sender_login']}</strong>.<br> If the selected folder is no longer "
                                f"relevant, the<br> connection with <strong>{self.__data['sender_login']}<br>"
                                f"</strong> will be terminated.</p>")

        self.accept_Button = QtWidgets.QPushButton(self)
        self.accept_Button.setGeometry(240, 273, 70, 30)
        self.accept_Button.setText('Accept')
        self.accept_Button.clicked.connect(self.accept)

        self.deny_Button = QtWidgets.QPushButton(self)
        self.deny_Button.setGeometry(320, 273, 70, 30)
        self.deny_Button.setText('Deny')
        self.deny_Button.clicked.connect(self.deny)

        self.list_checkBox = QtWidgets.QComboBox(self)
        self.list_checkBox.setGeometry(10, 238, 380, 25)
        check_font = QtGui.QFont()
        check_font.setBold(True)
        for i in range(self.__wpw.folders_tableWidget.rowCount()):
            if not self.__wpw.folders_tableWidget.item(i, 0) is None:
                if self.__wpw.folders_tableWidget.item(i, 0).font() == check_font:
                    self.list_checkBox.addItem(self.__wpw.folders_tableWidget.item(i, 0).text())
        if not self.list_checkBox.count():
            self.list_checkBox.addItem('Empty list')
            self.list_checkBox.setEnabled(False)
            self.accept_Button.setEnabled(False)

    def accept(self):
        data = {
            'sender_login': self.__data['receiver_login'],
            'sender_folder': self.list_checkBox.currentText(),
            'sender_mac': get_mac(),
            'choice': True,
            'receiver_login': self.__data['sender_login'],
            'receiver_folder': self.__data['sender_folder'],
            'receiver_id': self.__data['sender_id']
        }
        self.__socket.send_answer(data)
        self.__flag = False
        self.close()
        QTimer().singleShot(1500, self.__synchronize)

    def __synchronize(self):
        if synchronize_folder(
                sender_login=self.__wpw.login,
                receiver_id=self.__data['sender_id'],
                sender_folder=self.list_checkBox.currentText(),
                receiver_folder=self.__data['sender_folder'],
                token=self.__wpw.token
        ):
            threading.Thread(name='download_version', target=download_version, kwargs={
                'login': self.__wpw.login,
                'path': self.list_checkBox.currentText(),
                'token': self.__wpw.token,
                'flag': True
            }).start()

    def deny(self):
        self.__socket.send_answer({
            'sender_login': self.__data['receiver_login'],
            'choice': False,
            'receiver_login': self.__data['sender_login'],
        })
        self.__flag = False
        self.close()

    def closeEvent(self, event):
        if self.__flag:
            self.deny()
        self.__wpw.setEnabled(True)
