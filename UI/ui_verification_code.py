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

        self.code_LineEdit = QtWidgets.QLineEdit(self)
        self.code_LineEdit.setGeometry(10, 60, 275, 31)
        font.setPointSize(10)
        self.code_LineEdit.setFont(font)
        self.code_LineEdit.setPlaceholderText("Enter your code")

        self.enter_Button = QtWidgets.QPushButton(self)
        self.enter_Button.setGeometry(300, 60, 100, 31)
        font.setPointSize(8)
        self.enter_Button.setFont(font)
        self.enter_Button.setText("Enter")
        self.enter_Button.clicked.connect(self.enter)

        self.descripcion_Lable = QtWidgets.QLabel(self)
        self.descripcion_Lable.setGeometry(10, 10, 390, 41)
        font.setPointSize(9)
        self.descripcion_Lable.setFont(font)
        self.descripcion_Lable.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.descripcion_Lable.setWordWrap(True)
        self.descripcion_Lable.setText("The verification code has been sent to the specified mail. To complete the "
                                       "registration, enter it in the field below.")

    def enter(self):
        if self.code_LineEdit.text():
            self.suw.code = self.code_LineEdit.text()
            self.close()
