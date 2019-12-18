import sys

from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from board_widget import BoardWidget
from top_widget import TopWidget


class Center(QWidget):

    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        layout = QVBoxLayout()

        p = self.palette()
        p.setColor(QPalette.Background, QColor(192, 192, 192))
        self.setPalette(p)
        self.setAutoFillBackground(True)

        self.board = BoardWidget(16, 30, 99, parent=self)
        self.top = TopWidget(99, parent=self)

        layout.addWidget(self.top)
        layout.addWidget(self.board)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setCentralWidget(Center(parent=window))
    window.setWindowTitle('Definitely not minesweeper')
    window.show()
    sys.exit(app.exec_())
