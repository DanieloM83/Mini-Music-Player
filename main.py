from utils import StyleSheet
from widgets import PlayerFrame, MainFrame
from PyQt6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon, QActionGroup, QCursor
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
    Listener = None
    isRunning = True

    def __init__(self):
        super().__init__()
        try:
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

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.dragStartPosition = QCursor.pos()
        except Exception as ex:
            print(ex)

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == Qt.MouseButton.LeftButton:
                delta = event.globalPosition().toPoint() - self.dragStartPosition
                new_pos = self.pos() + delta
                right_down = self.pos() + delta + self.geometry().bottomRight()

                desktop = QApplication.primaryScreen()  # Или QGuiApplication.primaryScreen()
                available_rect = desktop.geometry()

                # Проверка и корректировка позиции окна
                if not available_rect.contains(new_pos):
                    new_pos.setX(max(available_rect.left(), min(new_pos.x(), available_rect.right() - self.width())))
                    new_pos.setY(max(available_rect.top(), min(new_pos.y(), available_rect.bottom() - self.height())))

                if not available_rect.contains(right_down):
                    new_pos.setX(max(available_rect.left(), min(new_pos.x(), available_rect.right() - self.width())))
                    new_pos.setY(max(available_rect.top(), min(new_pos.y(), available_rect.bottom() - self.height())))

                self.move(new_pos)
                self.dragStartPosition = QCursor.pos()
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    app = QApplication([])
    Window = MainWindow()

    sys.exit(app.exec())
