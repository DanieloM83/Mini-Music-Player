from PyQt6.QtWidgets import QListWidget, QToolButton, QFileDialog
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
from functional import StyleSheet
from widgets.base import BaseWidget
import json


class AddButton(QToolButton, BaseWidget):
    def __init__(self, parent):
        super(AddButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet('button.css') as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        icon = QIcon("style/resources/create.svg")
        self.setIcon(icon)
        self.resize_widget(0.63, 0.2, 0.25, 0.25, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly)
        if folder_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folder = folder_dialog.selectedFiles()[0]
            folder_name = selected_folder.split('/')[-1]
            data["PlayLists"].update({folder_name: selected_folder})
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            try:
                self.parent().rewrite_playlist()
            except Exception as ex:
                print(ex)


class DelButton(QToolButton, BaseWidget):
    def __init__(self, parent):
        super(DelButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet('button.css') as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        icon = QIcon("style/resources/delete.svg")
        self.setIcon(icon)
        self.resize_widget(0.63, 0.5, 0.25, 0.25, centered=True)
        self.released.connect(self.on_release)

    def on_release(self):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        playlists = self.parent().PlayLists
        try:
            del data["PlayLists"][playlists.currentItem().text()]
            self.parent().Player.stop()
        except Exception as ex:
            print(ex)
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        playlists.rewrite()


class PlayListSelector(QListWidget, BaseWidget):
    def __init__(self, parent):
        super(PlayListSelector, self).__init__(parent)
        self.ui_init()
        self.itemClicked.connect(self.handle_item_clicked)

    def ui_init(self):
        with StyleSheet("playlist.css") as style:
            self.setStyleSheet(style)
        self.resize_widget(0.83, 0.5, 0.3, 0.9, centered=True)
        self.rewrite()
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

    def rewrite(self):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.clear()
        items = data["PlayLists"]
        for name in items:
            self.addItem(name)
        if len(items) == 1:
            self.setCurrentRow(0)
            self.parent().Player.get_playlist(data["PlayLists"][self.currentItem().text()])

    def handle_item_clicked(self, item):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.parent().Player.get_playlist(data["PlayLists"][item.text()])
