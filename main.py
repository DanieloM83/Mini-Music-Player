from utils import StyleSheet
from widgets import PlayerFrame, MainFrame
from PyQt6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon, QActionGroup
from PyQt6.QtCore import Qt
from functools import partial
import sys
from pynput import keyboard
from functional import MusicPlayer


class MainWindow(QMainWindow):
    Tray = None
    Player_Frame = None
    Main_Frame = None
    Player = None
    Keyboard = None
    isRunning = True

    def __init__(self):
        super().__init__()
        try:
            self.Player = MusicPlayer(self)
            self.ui_init()
            self.tray_init()
            self.Player.start()
            listener = keyboard.Listener(on_release=lambda key: Window.shortcut_open(key))
            listener.start()
        except Exception as ex:
            print(ex)

    def ui_init(self):
        with StyleSheet("main_window.css") as style:
            self.setStyleSheet(style)

        self.setWindowTitle("Music Player")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.__resize_window(20, 18.5)
        self.Player_Frame = PlayerFrame(self)
        self.Main_Frame = MainFrame(self)
        self.show()

    def __resize_window(self, width_percent, height_percent):
        desktop = app.primaryScreen().size()
        w, h = desktop.width(), desktop.height()
        width = w * width_percent / 100
        height = h * height_percent / 100
        self.setGeometry(int(w - width) - 1, int(h - height), int(width) + 1, int(height) + 1)

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
            action.triggered.connect(partial(self.Main_Frame.add_gradient, color))
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
        self.isRunning = False
        self.Player.close()
        self.Keyboard.close()
        app.quit()

    def __tray_open(self, reason="ActivationReason.Trigger"):
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


if __name__ == "__main__":
    app = QApplication([])
    Window = MainWindow()

    sys.exit(app.exec())
