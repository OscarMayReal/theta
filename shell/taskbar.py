from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QAbstractSlider, QApplication, QWidget, QPushButton, QHBoxLayout

def main():
    app = QApplication([])
    window = QWidget()
    screen = app.primaryScreen()
    print(screen.availableSize().width())
    print(screen.availableSize().height())
    window.resize(screen.availableSize().width(), 40)
    window.move(10, 10)
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()

    row = QHBoxLayout()

    button = QPushButton("Quit")
    button.clicked.connect(app.quit)
    row.addWidget(button)

    window.setLayout(row)

    app.exec()

if __name__ == "__main__":
    main()
    