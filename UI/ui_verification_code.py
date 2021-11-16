from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow


class VCWindow(QMainWindow):
    def __init__(self, suw):
        super(VCWindow, self).__init__()
        self.suw = suw

        self.setWindowTitle('SyncGad • Verification code')
        self.setGeometry(600, 300, 410, 107)
        self.setFixedSize(self.size())

        font = QtGui.QFont()

        self.code_lineEdit = QtWidgets.QLineEdit(self)
        self.code_lineEdit.setGeometry(10, 60, 275, 31)
        font.setPointSize(10)
        self.code_lineEdit.setFont(font)
        self.code_lineEdit.setPlaceholderText("Enter your code")

        self.enter_Button = QtWidgets.QPushButton(self)
        self.enter_Button.setGeometry(300, 60, 100, 31)
        font.setPointSize(8)
        self.enter_Button.setFont(font)
        self.enter_Button.setText("Enter")
        self.enter_Button.clicked.connect(self.enter)

        self.description_Label = QtWidgets.QLabel(self)
        self.description_Label.setGeometry(10, 10, 390, 41)
        font.setPointSize(9)
        self.description_Label.setFont(font)
        self.description_Label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.description_Label.setWordWrap(True)
        self.description_Label.setText("The verification code has been sent to the specified mail. To complete the "
                                       "registration, enter it in the field below.")

    def enter(self):
        if self.code_lineEdit.text():
            self.suw.code = self.code_lineEdit.text()
            self.close()
