from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

def background():
    window = QWidget()
    window.showFullScreen()
    layout = QHBoxLayout(window)
    maincontainer = QWidget()
    maincontainer.setFixedWidth(1920)
    maincontainer.setFixedHeight(1080)
    background = QWidget()
    background.setStyleSheet("background-color: #000000;")
    layout.addWidget(background, 1)
    layout.addWidget(maincontainer, 2)
    return window, maincontainer

app = QApplication([])
window, maincontainer = background()
app.exec()
