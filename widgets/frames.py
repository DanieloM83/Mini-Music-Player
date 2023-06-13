from PyQt6.QtWidgets import QFrame, QApplication
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from functional import StyleSheet
from widgets.base import BaseWidget
from widgets.player_btn import PlayButton, PrevButton, NextButton
from widgets.player_slider import MusicSlider, Labels
from widgets.volume import VolumeSlider, VolumeButton
from widgets.playlist_btn import AddButton, DelButton, PlayListSelector
import json


class MainFrame(QFrame, BaseWidget):
    Player = None

    PlayLists = None
    AddButton = None
    DelButton = None
    Drag = None

    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Player = parent.Player
        self.ui_init()

    def ui_init(self):
        with StyleSheet("main_frame.css") as style:
            self.setStyleSheet(style)
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.resize_widget(0, 0, 1, 0.625)
        self.change_theme(data["Theme"])

        self.PlayLists = PlayListSelector(self)
        self.AddButton = AddButton(self)
        self.DelButton = DelButton(self)

    def change_theme(self, color):
        style_sheet = self.styleSheet()
        updated = style_sheet + '''QFrame { background-color: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
        stop: 0 ''' + color + ''', stop: 1 #121212); }'''
        self.setStyleSheet(updated)

    def rewrite_playlist(self):
        self.PlayLists.rewrite()

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.Drag = QCursor.pos()
        except Exception as ex:
            print(ex)

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == Qt.MouseButton.LeftButton:
                delta = event.globalPosition().toPoint() - self.Drag
                new_pos = self.parent().pos() + delta
                right_down = self.parent().pos() + delta + self.geometry().bottomRight()

                desktop = QApplication.primaryScreen()
                available_rect = desktop.geometry()
                if not available_rect.contains(new_pos):
                    new_pos.setX(
                        max(available_rect.left(), min(new_pos.x(), available_rect.right() - self.parent().width())))
                    new_pos.setY(
                        max(available_rect.top(), min(new_pos.y(), available_rect.bottom() - self.parent().height())))

                if not available_rect.contains(right_down):
                    new_pos.setX(
                        max(available_rect.left(), min(new_pos.x(), available_rect.right() - self.parent().width())))
                    new_pos.setY(
                        max(available_rect.top(), min(new_pos.y(), available_rect.bottom() - self.parent().height())))

                self.parent().move(new_pos)
                self.Drag = QCursor.pos()
        except Exception as ex:
            print(ex)


class PlayerFrame(QFrame, BaseWidget):
    Player = None

    VolumeButton = None
    VolumeSlider = None
    MusicSlider = None
    PlayButton = None
    PrevButton = None
    NextButton = None
    Labels = None

    def __init__(self, parent):
        super(PlayerFrame, self).__init__(parent)
        self.Player = parent.Player
        self.ui_init()

    def ui_init(self):
        with StyleSheet("player.css") as style:
            self.setStyleSheet(style)

        self.resize_widget(0, 0.625, 1, 0.375)

        self.VolumeSlider = VolumeSlider(self)
        self.VolumeButton = VolumeButton(self)

        self.MusicSlider = MusicSlider(self)
        self.Labels = Labels(self)

        self.PlayButton = PlayButton(self)
        self.PrevButton = PrevButton(self)
        self.NextButton = NextButton(self)
