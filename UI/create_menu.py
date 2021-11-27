from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon


def du_menu(obj):
    obj.menuBar = QMenuBar(obj)
    obj.setMenuBar(obj.menuBar)

    profile_menu = QMenu('&Profile', obj)
    obj.menuBar.addMenu(profile_menu)

    changepass_action = QAction(QIcon('icons/menu/change_password.svg'), '&Change password', obj)
    changepass_action.setStatusTip('Change the password')
    changepass_action.triggered.connect(obj.change_password)

    delac_action = QAction(QIcon('icons/menu/delete_account.svg'), '&Delete account', obj)
    delac_action.setStatusTip('Delete your account')
    delac_action.triggered.connect(obj.delete_account)

    showsync_action = QAction(QIcon('icons/menu/show_synchronized.svg'), 'Show synchronized folders', obj)
    showsync_action.setStatusTip('show')
    showsync_action.triggered.connect(obj.show_synchronized)

    exitpr_action = QAction(QIcon('icons/menu/exit_profile.svg'), '&Exit profile', obj)
    exitpr_action.setStatusTip('Exit to sign in window')
    exitpr_action.triggered.connect(obj.exit_profile)

    profile_menu.addAction(changepass_action)
    profile_menu.addAction(delac_action)
    profile_menu.addSeparator()
    profile_menu.addAction(showsync_action)
    profile_menu.addSeparator()
    profile_menu.addAction(exitpr_action)

    help_menu = QMenu('&Help', obj)
    obj.menuBar.addMenu(help_menu)

    about_action = QAction(QIcon('icons/menu/about.svg'), '&About', obj)
    about_action.setStatusTip('About this application')
    about_action.triggered.connect(obj.about)

    exit_action = QAction(QIcon('icons/menu/exit.svg'), '&Exit', obj)
    exit_action.setStatusTip('Quit this application')
    exit_action.triggered.connect(obj.exit)

    help_menu.addAction(about_action)
    help_menu.addSeparator()
    help_menu.addAction(exit_action)


def un_menu(obj):
    obj.menuBar = QMenuBar(obj)
    obj.setMenuBar(obj.menuBar)

    help_menu = QMenu('&Help', obj)
    obj.menuBar.addMenu(help_menu)

    about_action = QAction(QIcon('icons/menu/about.svg'), '&About', obj)
    about_action.setStatusTip('About this application')
    about_action.triggered.connect(obj.about)

    exit_action = QAction(QIcon('icons/menu/exit.svg'), '&Exit', obj)
    exit_action.setStatusTip('Quit this application')
    exit_action.triggered.connect(obj.exit)

    help_menu.addAction(about_action)
    help_menu.addSeparator()
    help_menu.addAction(exit_action)

    return help_menu
