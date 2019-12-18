from PySide2.QtCore import QTime
from PySide2.QtGui import QIcon, Qt, QPalette
from PySide2.QtWidgets import QFrame, QToolButton, QHBoxLayout, QLCDNumber
from PySide2.QtCore import QTimerEvent


class CustomTimer(QLCDNumber):
    def __init__(self, interval: int, parent=None):
        super(CustomTimer, self).__init__(parent)
        self.time = QTime()
        self.interval = interval

        p = self.palette()
        p.setColor(QPalette.Background, Qt.black)
        p.setColor(p.Light, Qt.darkRed)
        self.setPalette(p)

        self.timer = None

    def timerEvent(self, event: QTimerEvent):
        self.display(int(self.time.elapsed()/self.interval))

    def start(self):
        self.timer = self.startTimer(int(self.interval / 2))
        self.time.start()

    def stop(self):
        if self.timer is not None:
            self.killTimer(self.timer)

    def reset(self):
        self.display(0)


class TopWidget(QFrame):
    # TODO: Use Qt's embedded resources for images and icons
    _icon_locations = {
        'smile': './assets/smile.jpg',
        'open': './assets/open.jpg',
        'dead': './assets/dead.jpg'
    }

    def __init__(self, bomb_count: int, parent=None):
        super(TopWidget, self).__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.center = parent

        self.bombCounter = QLCDNumber(len(str(bomb_count))+1)
        p = self.bombCounter.palette()
        p.setColor(QPalette.Background , Qt.black)
        p.setColor(p.Light, Qt.darkRed)
        self.bombCounter.setPalette(p)
        self.bombCounter.display(bomb_count)

        self.resetButton = QToolButton()
        self.resetButton.setIcon(QIcon(self._icon_locations['smile']))
        self.resetButton.clicked.connect(self.center.board.reset_board)

        self.timer = CustomTimer(1000)

        upper_layout = QHBoxLayout()
        upper_layout.setMargin(5)
        upper_layout.addWidget(self.bombCounter)
        upper_layout.addWidget(self.resetButton)
        upper_layout.addWidget(self.timer)
        upper_layout.setAlignment(self.bombCounter, Qt.AlignLeft)
        upper_layout.setAlignment(self.resetButton, Qt.AlignHCenter)
        upper_layout.setAlignment(self.timer, Qt.AlignRight)

        self.setLayout(upper_layout)

    def update_counter(self, counter: int):
        self.bombCounter.display(counter)

    def kill_smile(self):
        self.resetButton.setIcon(QIcon(self._icon_locations['dead']))

    def revive_smile(self):
        self.resetButton.setIcon((QIcon(self._icon_locations['smile'])))
