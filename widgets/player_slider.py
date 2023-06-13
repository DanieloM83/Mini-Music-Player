from PyQt6.QtWidgets import QSlider, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from functional import StyleSheet
from widgets.base import BaseWidget
import json


class MusicSlider(QSlider, BaseWidget):
    def __init__(self, parent):
        super(MusicSlider, self).__init__(parent)
        self.ui_init()
        self.mousePressEvent = self.pressed
        self.enterEvent = self.hover
        self.leaveEvent = self.un_hover

    def ui_init(self):
        with StyleSheet('slider.css') as style:
            self.setStyleSheet(style)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.resize_widget(0.5, 0.75, 0.5, 0.1, centered=True)

    def pressed(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pixel_value = event.pos().x()  # Получение значения слайдера в пиксельных координатах
            slider_value = self.minimum() + int(pixel_value / self.width() * (
                    self.maximum() - self.minimum()))  # Перевод пиксельных координат в значение слайдера
            self.setValue(slider_value)
            self.parent().parent().Player.set_pos(slider_value)

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


class Labels(BaseWidget):
    StartLab = None
    EndLab = None

    def __init__(self, parent):
        super(Labels, self).__init__()
        self.parent = parent
        self.ui_init()

    def ui_init(self):
        self.StartLab = QLabel("0:00", self.parent)
        self.EndLab = QLabel("0:00", self.parent)

        self.StartLab.setFont(QFont("style/resources/Nunito-Bold.ttf", 10, QFont.Weight.Bold))
        self.StartLab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.StartLab.setStyleSheet("color: white;")

        self.EndLab.setFont(QFont("style/resources/Nunito-Bold.ttf", 10, QFont.Weight.Bold))
        self.EndLab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.EndLab.setStyleSheet("color: white;")

        self.StartLab.setGeometry(*self.calculate(0.185, 0.75, 0.12, 0.12, parent=self.parent, centered=True).values())
        self.EndLab.setGeometry(*self.calculate(0.815, 0.75, 0.12, 0.12, parent=self.parent, centered=True).values())

    def set_text(self, start_text, end_text):
        self.StartLab.setText(start_text)
        self.EndLab.setText(end_text)
