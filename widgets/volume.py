from PyQt6.QtWidgets import QToolButton, QSlider
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from functional import StyleSheet
from widgets.base import BaseWidget
import json


class VolumeButton(QToolButton, BaseWidget):
    isMuted = False

    def __init__(self, parent):
        super(VolumeButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        icon = QIcon("style/resources/volume4.svg")
        self.setIcon(icon)
        self.resize_widget(0.72, 0.33, 0.1, 0.4, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        if self.isMuted:
            # включи звук, сверяясь с бегунком
            self.isMuted = False
            volume = self.parent().VolumeSlider.value()
            self.set_icon(volume)
            self.set_volume(volume)
        else:
            # выключи звук
            self.isMuted = True
            self.set_icon(0)
            self.set_volume(0)

    def set_icon(self, value):
        if value == 0:
            self.setIcon(QIcon("style/resources/volume1.svg"))
        elif value < 33:
            self.setIcon(QIcon("style/resources/volume2.svg"))
        elif value < 66:
            self.setIcon(QIcon("style/resources/volume3.svg"))
        else:
            self.setIcon(QIcon("style/resources/volume4.svg"))

        if value != 0:
            self.isMuted = False

        self.set_volume(value)

    def set_volume(self, volume):
        self.parent().Player.set_volume(volume)


class VolumeSlider(QSlider, BaseWidget):
    def __init__(self, parent):
        super(VolumeSlider, self).__init__(parent)
        self.ui_init()
        self.mousePressEvent = self.sliderMousePressEvent
        self.enterEvent = self.hover
        self.leaveEvent = self.un_hover
        self.setMaximum(100)
        self.setValue(100)

    def ui_init(self):
        with StyleSheet('slider.css') as style:
            self.setStyleSheet(style)

        self.setOrientation(Qt.Orientation.Horizontal)
        self.resize_widget(0.77, 0.3, 0.21, 0.1)

    def sliderMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pixelValue = event.pos().x()
            sliderValue = self.minimum() + int(pixelValue / self.width() * (self.maximum() - self.minimum()))
            self.setValue(sliderValue)
            self.parent().VolumeButton.set_icon(sliderValue)

    def hover(self, event):
        with open("config.json", "r", encoding="utf-8") as style:
            data = json.load(style)
        now = self.styleSheet()
        self.setStyleSheet(now + "QSlider::handle:horizontal { width: 12px; }" +
                           "QSlider::sub-page {background-color:" + data["Theme"] + ";}")

    def un_hover(self, event):
        now = self.styleSheet()
        self.setStyleSheet(now + "QSlider::handle:horizontal { width: 0px; }" +
                           "QSlider::sub-page {background-color:white;}")
