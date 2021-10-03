from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon


def du_menu(obj):
    obj.menuBar = QMenuBar(obj)
    obj.setMenuBar(obj.menuBar)

    profileMenu = QMenu('&Profile', obj)
    obj.menuBar.addMenu(profileMenu)

    changepassAction = QAction(QIcon('icons/change_password.svg'), '&Change password', obj)
    changepassAction.setStatusTip('Change the password')
    changepassAction.triggered.connect(obj.change_password)

    changemailAction = QAction(QIcon('icons/change_mail.svg'), '&Change mail', obj)
    changemailAction.setStatusTip('Change the mail address')
    changemailAction.triggered.connect(obj.change_mail)

    delacAction = QAction(QIcon('icons/delete_account.svg'), '&Delete account', obj)
    delacAction.setStatusTip('Delete your account')
    delacAction.triggered.connect(obj.delete_account)

    exitprAction = QAction(QIcon('icons/exit_profile.svg'), '&Exit profile', obj)
    exitprAction.setStatusTip('Exit to sign in window')
    exitprAction.triggered.connect(obj.exit_profile)

    profileMenu.addAction(changepassAction)
    profileMenu.addAction(changemailAction)
    profileMenu.addAction(delacAction)
    profileMenu.addSeparator()
    profileMenu.addAction(exitprAction)

    helpMenu = QMenu('&Help', obj)
    obj.menuBar.addMenu(helpMenu)

    aboutAction = QAction(QIcon('icons/about.svg'), '&About', obj)
    aboutAction.setStatusTip('About this application')
    aboutAction.triggered.connect(obj.about)

    exitAction = QAction(QIcon('icons/exit.svg'), '&Exit', obj)
    exitAction.setStatusTip('Quit this application')
    exitAction.triggered.connect(obj.exit)

    helpMenu.addAction(aboutAction)
    helpMenu.addSeparator()
    helpMenu.addAction(exitAction)


def un_menu(obj):
    obj.menuBar = QMenuBar(obj)
    obj.setMenuBar(obj.menuBar)

    helpMenu = QMenu('&Help', obj)
    obj.menuBar.addMenu(helpMenu)

    aboutAction = QAction(QIcon('icons/about.svg'), '&About', obj)
    aboutAction.setStatusTip('About this application')
    aboutAction.triggered.connect(obj.about)

    exitAction = QAction(QIcon('icons/exit.svg'), '&Exit', obj)
    exitAction.setStatusTip('Quit this application')
    exitAction.triggered.connect(obj.exit)

    helpMenu.addAction(aboutAction)
    helpMenu.addSeparator()
    helpMenu.addAction(exitAction)
