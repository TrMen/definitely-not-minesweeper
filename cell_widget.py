from PySide2.QtGui import QPaintEvent, QPainter, QColor, QBrush, QFontDatabase, QMouseEvent, \
    QImage
from PySide2.QtWidgets import QSizePolicy, QFrame, QApplication
from PySide2.QtCore import Qt, QEvent, QPoint


class CellWidget(QFrame):
    _bg = QColor(192, 192, 192)  # darkgray
    content_colors = {
        '1': QColor(0, 0, 255),  # blue
        '2': QColor(0, 128, 0),  # green
        '3': QColor(255, 0, 0),  # red
        '4': QColor(0, 0, 128),  # navy
        '5': QColor(128, 0, 0),  # maroon
        '6': QColor(255, 0, 0),  # red
        '7': QColor(255, 0, 0),  # red
        '8': QColor(255, 0, 0)  # red

    }
    image_locations = {
        'flag': './assets/flag.jpg',
        'bomb': './assets/bomb.jpg',
        'exploded_bomb': './assets/exploded_bomb.jpg',
        'false_bomb' : './assets/false_bomb.jpg'

    }

    def __init__(self, index: int, parent=None):
        super(CellWidget, self).__init__(parent)
        self.grid = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.ClickFocus)
        self.mode = 'hidden'
        self.content = None
        self.index = index
        self.was_clicked_bomb = False
        self.locked = False

    def reset(self):
        self.mode = 'hidden'
        self.content = None
        self.was_clicked_bomb = False
        self.locked = False
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.type() == QEvent.MouseButtonPress:
            if self.locked:
                return
            if self.mode == 'hidden':
                if event.button() == Qt.LeftButton:
                    if not self.grid.in_progress:
                        self.grid.start_game()

                    self.mode = 'revealed'
                    if self.content == 'bomb':
                        self.grid.clicked_bomb(self.index)

                    if self.content == '0':
                        self.propagate_click()

                    self.update()

            if event.button() == Qt.RightButton:
                if self.mode in ['flag', 'hidden']:
                    self.grid.flag_update(self.index)
                    self.update()

    def propagate_click(self):
        min_w = -1 if self.index % self.grid.width != 0 else 0
        max_w = 2 if self.index % self.grid.width != self.grid.width - 1 else 1
        for h in range(-1, 2):
            for w in range(min_w, max_w):
                neighbor_index = self.index + self.grid.width * h + w
                if neighbor_index in range(0, len(self.grid.cells)):
                    if self.grid.cells[neighbor_index].mode == 'hidden':
                        event = QMouseEvent(QEvent.MouseButtonPress, QPoint(0, 0),
                                            Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
                        QApplication.sendEvent(self.grid.cells[neighbor_index], event)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.eraseRect(event.rect())

        painter.setBrush(QBrush(self._bg))
        painter.drawRect(event.rect())

        if self.mode == 'revealed':
            self.setFrameStyle(QFrame.Panel | QFrame.Plain)
            self.setLineWidth(0)
            self.setMidLineWidth(0)
            if self.content in self.content_colors.keys():
                font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
                font.setPixelSize(int(self.width() * 5 / 6))
                painter.setPen(self.content_colors[self.content])
                painter.setFont(font)
                flags = Qt.AlignCenter | Qt.TextJustificationForced
                painter.drawText(event.rect(), flags, self.content)

            if self.content == 'bomb':
                loc = 'exploded_bomb' if self.was_clicked_bomb else 'bomb'
                painter.drawImage(event.rect(), QImage(self.image_locations[loc]))

        if self.mode == 'hidden':
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(3)
            self.setMidLineWidth(2)

        if self.mode == 'false_bomb':
            painter.drawImage(event.rect(), QImage(self.image_locations['false_bomb']))

        if self.mode == 'flag':
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(3)
            self.setMidLineWidth(2)
            painter.drawImage(event.rect(), QImage(self.image_locations['flag']))

        super(CellWidget, self).paintEvent(event)
