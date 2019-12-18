import sys

from PySide2.QtCore import QSize
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from cell_widget import CellWidget
import random


class BoardWidget(QFrame):
    def __init__(self, width: int, height: int, bomb_count: int, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        if bomb_count > height*width:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Nuh')
            msg_box.setText('Too many bombs for your board!')
            msg_box.exec()
            sys.exit()

        p = self.palette()
        p.setColor(QPalette.Background, QColor(192, 192, 192))
        self.setPalette(p)
        self.setAutoFillBackground(True)

        self.center = parent
        self.height = height
        self.width = width
        self.cells = [CellWidget(i, parent=self) for i in range(width*height)]
        self.generate_layout()
        self.flag_count = 0
        self.bomb_count = bomb_count
        self.init_board()

        self.in_progress = False

    def generate_layout(self):
        layout = QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(0)
        for row in range(self.height):
            row_layout = QVBoxLayout()
            row_layout.setMargin(0)
            row_layout.setSpacing(0)
            for col in range(self.width):
                row_layout.addWidget(self.cells[row * self.width + col])
            layout.addLayout(row_layout)

        self.setLayout(layout)

    def reset_board(self):
        for cell in self.cells:
            cell.reset()
        self.init_board()
        self.center.top.timer.reset()
        self.in_progress = False
        self.center.top.revive_smile()
        self.center.top.timer.stop()

    def start_game(self):
        self.in_progress = True
        self.center.top.timer.start()

    def end_game(self):
        self.in_progress = False
        self.center.top.timer.stop()
        for cell in self.cells:
            cell.locked = True

    def clicked_bomb(self, index: int):
        self.cells[index].was_clicked_bomb = True
        self.center.top.kill_smile()
        for cell in self.cells:
            if cell.content == 'bomb':
                cell.mode = 'revealed'
            if cell.mode == 'flag':
                if cell.content != 'bomb':
                    cell.mode = 'false_bomb'
            cell.update()

        self.end_game()

    def sizeHint(self) -> QSize:
        return QSize(self.height * 30, self.width * 30)

    def flag_update(self, index: int):
        hidden = self.cells[index].mode == 'hidden'
        self.cells[index].mode = 'flag' if hidden else 'hidden'
        if hidden:
            self.flag_count += 1
        else:
            self.flag_count -= 1
        self.center.top.update_counter(self.bomb_count - self.flag_count)
        if self.bomb_count - self.flag_count <= 0:
            self.check_victory()

    def check_victory(self):
        if all([c.content == 'bomb' for c in self.cells if c.mode == 'flag']):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Victory!')
            msg_box.setText('You identified all bombs!')
            self.end_game()
            msg_box.exec()

    def init_board(self):
        # TODO: Make this actually only generate solvable games
        # Init bombs
        sample = random.sample(self.cells, self.bomb_count)
        for cell in self.cells:
            if cell in sample:
                cell.content = 'bomb'

        # Init numbers
        for cell in self.cells:
            if cell.content != 'bomb':
                cell.content = str(self.neighbor_bombs(cell.index))

    def neighbor_bombs(self, index: int):
        # TODO: This isn't good. It's way too hard to understand
        count = 0
        min_w = -1 if index % self.width != 0 else 0  # Ignore left elements if leftmost in row
        max_w = 2 if index % self.width != self.width - 1 else 1  # Ignore right elements if rightmost in row
        for h in range(-1, 2):
            for w in range(min_w, max_w):
                neighbor_index = index + self.width * h + w
                if neighbor_index in range(0, len(self.cells)):
                    if self.cells[neighbor_index].content == 'bomb':
                        count += 1
        return count
