from databases.db_action import create, show
from UI.ui_sign_in import sign_in_window

if __name__ == '__main__':
    conn = create()
    show(conn)
    sign_in_window(conn)
