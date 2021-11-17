from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow

from UI.call_ui import show_dialog
from UI_functional.synchronized import synchronize_folder
from UI_functional.workplace import download_version
from data_processing.get_folder_data import get_mac


class ASWindow(QMainWindow):
    def __init__(self, text, wpw):
        super(ASWindow, self).__init__()
        self.__text = text
        self.__wpw = wpw
        self.__socket = wpw.socket
        self.__flag = True

        self.__wpw.setEnabled(False)

        self.setWindowTitle('SyncGad • Accepting')
        self.setGeometry(400, 400, 400, 263)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(12)

        self.desc_Label = QtWidgets.QLabel(self)
        self.desc_Label.setGeometry(10, 3, 390, 180)
        self.desc_Label.setFont(font)
        self.desc_Label.setText(f"<h4 style='text-align: justify;'>User <span style='color: #999999;'>"
                                f"<em>{self.__text['current_user']}</em></span> want to synchronize his local "
                                f"folder<br> <span style='color: #999999;'><em>{self.__text['current_folder']}"
                                f"</em></span> with you.</h4><p style='text-align: justify;'>To accept the request, "
                                f"select the appropriate folder<br> from the list of relevant ones below. Now and in"
                                f"<br> the future, during authorization, the contents of<br> your folder will be "
                                f"automatically updated according<br> to the contents of the user`s folder <strong>"
                                f"{self.__text['current_user']}</strong>. If the<br> selected folder is no longer "
                                f"relevant, the connection<br> with <strong>{self.__text['current_user']}"
                                f"</strong> will be terminated.</p>")

        self.accept_Button = QtWidgets.QPushButton(self)
        self.accept_Button.setGeometry(240, 223, 70, 30)
        self.accept_Button.setText('Accept')
        self.accept_Button.clicked.connect(self.accept)

        self.deny_Button = QtWidgets.QPushButton(self)
        self.deny_Button.setGeometry(320, 223, 70, 30)
        self.deny_Button.setText('Deny')
        self.deny_Button.clicked.connect(self.deny)

        self.list_checkBox = QtWidgets.QComboBox(self)
        self.list_checkBox.setGeometry(10, 188, 380, 25)
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
        self.__socket.send_answer({
            'current_user': self.__text['other_user'],
            'current_folder': self.list_checkBox.currentText(),
            'current_mac': get_mac(),
            'choice': True,
            'other_user': self.__text['current_user'],
            'other_folder': self.__text['current_folder'],
            'other_mac': self.__text['current_mac']
        })
        self.__flag = False
        self.close()
        QTimer().singleShot(1500, self.__synchronize())

    def __synchronize(self):
        if synchronize_folder(
                current_login=self.login,
                other_login=self.__text['current_user'],
                current_folder=self.list_checkBox.currentText(),
                other_folder=self.__text['current_folder'],
                token=self.token
        ):
            if not download_version(
                    login=self.login,
                    path=self.list_checkBox.currentText(),
                    token=self.token,
                    flag=True
            ):
                show_dialog('Error', 'Error occurred while synchronizing.\nProcess was stopped.')

    def deny(self):
        self.__socket.send_answer({
            'current_user': self.__text['other_user'],
            'choice': False,
            'other_user': self.__text['current_user'],
        })
        self.__flag = False
        self.close()

    def closeEvent(self, event):
        if self.__flag:
            self.deny()
        self.__wpw.setEnabled(True)
