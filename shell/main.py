import subprocess
import pam
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
import pwd, os


def Login(username, password):
    if pam.authenticate(username, password):
        print("Authentication successful")
    else:
        print("Authentication failed")


def do_login(username, password, statustext, app, window):
    if pam.authenticate(username.currentText(), password.text()):
        statustext.setText("Login successful")
        username.clear()
        password.clear()
        window.close()
        os.system(".venv/bin/python3 taskbar.py")
        app.quit()
    else:
        statustext.setText("Login failed")

def main():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Login")

    # username = QLineEdit()
    # username.setPlaceholderText("Username")
    username = QComboBox()
    for user in pwd.getpwall():
        username.addItem(user.pw_name)

    password = QLineEdit()
    password.setPlaceholderText("Password")
    password.setEchoMode(QLineEdit.Password)

    statustext = QLabel()
    statustext.setAlignment(Qt.AlignCenter)

    loginbutton = QPushButton("Login")
    loginbutton.clicked.connect(lambda: do_login(username, password, statustext, app, window))

    layout = QVBoxLayout()
    layout.addWidget(username)
    layout.addWidget(password)
    layout.addWidget(loginbutton)
    layout.addWidget(statustext)
    window.setLayout(layout)
    window.showFullScreen()
    app.exec()

if __name__ == "__main__":
    main()
