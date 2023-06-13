from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from functional import StyleSheet
from widgets.base import BaseWidget


class PlayButton(QToolButton, BaseWidget):
    IconType = None

    def __init__(self, parent):
        super(PlayButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        self.IconType = "play"

        self.setIcon(QIcon("style/resources/play.svg"))
        self.resize_widget(0.5, 0.33, 0.1, 0.56, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        if not self.parent().Player.isstop:
            self.parent().Player.play_stop()
            if self.IconType == "play":
                self.IconType = "pause"
                self.setIcon(QIcon("style/resources/pause.svg"))
            else:
                self.IconType = "play"
                self.setIcon(QIcon("style/resources/play.svg"))


class NextButton(QToolButton, BaseWidget):
    def __init__(self, parent):
        super(NextButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        self.setIcon(QIcon("style/resources/next.svg"))
        self.resize_widget(0.6, 0.33, 0.12, 0.54, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        self.parent().Player.next()


class PrevButton(QToolButton, BaseWidget):
    def __init__(self, parent):
        super(PrevButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        icon = QIcon("style/resources/prev.svg")
        self.setIcon(icon)
        self.resize_widget(0.4, 0.33, 0.12, 0.54, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        self.parent().Player.prev()
