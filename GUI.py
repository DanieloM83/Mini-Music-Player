from functional import StyleSheet
from widgets import base, frames
from PyQt6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon, QActionGroup
from PyQt6.QtCore import Qt
from functools import partial
import sys
import json
from pynput import keyboard
from functional import MusicPlayer


class MainWindow(QMainWindow, base.BaseWidget):
    PlayerFrame = None
    MainFrame = None
    Listener = None
    Player = None
    Tray = None
    isRunning = False

    def __init__(self):
        super().__init__()
        try:
            self.isRunning = True
            self.Player = MusicPlayer(self)
            self.ui_init()
            self.tray_init()
            self.Player.start()
            self.Listener = keyboard.Listener(on_release=lambda key: Window.shortcut_open(key))
            self.Listener.start()
        except Exception as ex:
            print(ex)

    def ui_init(self):
        with StyleSheet("main_window.css") as style:
            self.setStyleSheet(style)

        self.setWindowIcon(QIcon("style/resources/Player.ico"))
        self.setWindowTitle("Music Player")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.resize_widget(0.7994, 0.8148, 0.2006, 0.186, parent=app.primaryScreen())

        self.PlayerFrame = frames.PlayerFrame(self)
        self.MainFrame = frames.MainFrame(self)

        self.show()

    def tray_init(self):
        with StyleSheet('tray.css') as style:
            app.setStyleSheet(style)
        tray = QSystemTrayIcon()
        self.Tray = tray
        icon = QIcon('style/resources/Player.ico')
        tray.setIcon(icon)
        tray.setToolTip("Music Player")
        menu = QMenu()
        menu.addAction(QAction("Show/Hide", menu, triggered=self.open))

        submenu = QMenu("Theme", menu)

        action_group = QActionGroup(submenu)

        for name, color in [["Red", "#FF0000"], ["Blue", "#0000FF"], ["Yellow", "#FFFF00"], ["Green", "#00FF00"]]:
            action = QAction(name, submenu)
            action.triggered.connect(partial(self.change_theme, color))
            action.setCheckable(True)
            action_group.addAction(action)
            submenu.addAction(action)

        menu.addMenu(submenu)

        menu.addSeparator()
        menu.addAction(QAction("Exit", menu, triggered=self.tray_close))
        tray.setContextMenu(menu)
        tray.activated.connect(self.__tray_open)

        tray.show()

    def tray_close(self):
        try:
            self.isRunning = False
            self.Player.quit()
            self.Listener.stop()
            self.Tray.hide()
            self.Tray.deleteLater()
            app.quit()
        except Exception as ex:
            print(ex)

    def __tray_open(self, reason):
        if str(reason) == "ActivationReason.Trigger":
            if self.isVisible():
                return self.setVisible(False)
            self.setVisible(True)

    def open(self):
        if self.isVisible():
            return self.setVisible(False)
        self.setVisible(True)

    def shortcut_open(self, key):
        if str(key) == "Key.f8":
            if self.isVisible():
                return self.setVisible(False)
            self.setVisible(True)

    def change_theme(self, color):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.MainFrame.change_theme(color)
        data["Theme"] = color
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    app = QApplication([])
    Window = MainWindow()

    sys.exit(app.exec())
