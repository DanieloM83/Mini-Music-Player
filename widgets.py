from PyQt6.QtWidgets import QFrame, QListWidget, QToolButton, QSlider, QFileDialog
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt
from utils import StyleSheet
import json


class MainFrame(QFrame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("main_frame.css") as style:
            self.setStyleSheet(style)
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.add_gradient(data["Theme"])

        self.__resize_frame(100, 62.5)
        self.combobox = PlayListSelector(self)
        self.addbutton = AddButton(self)
        self.deletbutton = DelButton(self)

    def __resize_frame(self, width_percent, height_percent):
        pg = self.parent().geometry()
        w, h = pg.width(), pg.height()
        width = w * width_percent / 100
        height = h * height_percent / 100
        self.setGeometry(0, 0, int(width), int(height))

    def add_gradient(self, color):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        style_sheet = self.styleSheet()
        updated = style_sheet + '''QFrame { background-color: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
        stop: 0 ''' + color + ''', stop: 1 #121212); }'''
        self.setStyleSheet(updated)
        data["Theme"] = color
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class PlayerFrame(QFrame):
    def __init__(self, parent):
        super(PlayerFrame, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("player.css") as style:
            self.setStyleSheet(style)

        self.__resize_frame(100, 37.5)
        self.playbutton = PlayButton(self)
        self.nextbutton = NextButton(self)
        self.prevbutton = PrevButton(self)
        self.musicslider = MusicSlider(self)

    def __resize_frame(self, width_percent, height_percent):
        pg = self.parent().geometry()
        w, h = pg.width(), pg.height()
        width = w * width_percent / 100
        height = h * height_percent / 100
        self.setGeometry(0, int(h - height), int(width), int(height))


class PlayListSelector(QListWidget):
    def __init__(self, parent):
        super(PlayListSelector, self).__init__(parent)
        self.ui_init()
        self.itemClicked.connect(self.handle_item_clicked)

    def ui_init(self):
        with StyleSheet("playlist.css") as style:
            self.setStyleSheet(style)
        self.__resize_box(30, 100)
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

    def handle_item_clicked(self, item):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.parent().parent().Player.get_playlist(data["PlayLists"][item.text()])

    def __resize_box(self, width_percent, height_percent):
        pg = self.parent().geometry()
        w, h = pg.width(), pg.height()
        width = int(w * width_percent / 100)
        height = int(h - 10)
        self.setGeometry(w - 5 - width, 5, width, height)


class PlayButton(QToolButton):
    def __init__(self, parent):
        super(PlayButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        self.icon_name = "play"
        self.setIcon(QIcon("style/resources/play.svg"))
        self.__resize_button(10.3896)
        self.released.connect(self.on_release)

    def __resize_button(self, percent):
        pg = self.parent().geometry()
        w = pg.width()
        width = w * percent / 100
        height = width
        self.setGeometry(int(w // 2 - width // 2), 5, int(width), int(height))

    def on_release(self):
        self.parent().parent().Player.play_stop()
        if self.icon_name == "play":
            self.icon_name = "pause"
            self.setIcon(QIcon("style/resources/pause.svg"))
        else:
            self.icon_name = "play"
            self.setIcon(QIcon("style/resources/play.svg"))


class NextButton(QToolButton):
    def __init__(self, parent):
        super(NextButton, self).__init__(parent)
        self.ui_init()

    def ui_init(self):
        with StyleSheet("button.css") as style:
            self.setStyleSheet(style)

        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        self.setIcon(QIcon("style/resources/next.svg"))
        self.__resize_button(10)
        self.released.connect(self.on_release)

    def __resize_button(self, percent):
        add = self.parent().playbutton.size().width()

        pg = self.parent().geometry()
        w = pg.width()
        width = w * percent / 100
        height = width
        self.setGeometry(int(w // 2 - width // 2 + add), 5, int(width), int(height))

    def on_release(self):
        self.parent().parent().Player.next()


class PrevButton(QToolButton):
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
        self.__resize_button(10)
        self.released.connect(self.on_release)

    def __resize_button(self, percent):
        add = self.parent().playbutton.size().width()

        pg = self.parent().geometry()
        w = pg.width()
        width = w * percent / 100
        height = width
        self.setGeometry(int(w // 2 - width // 2 - add), 5, int(width), int(height))

    def on_release(self):
        self.parent().parent().Player.prev()


class MusicSlider(QSlider):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_init()
        self.mousePressEvent = self.sliderMousePressEvent
        self.enterEvent = self.sliderEnterEvent
        self.leaveEvent = self.sliderLeaveEvent
        self.setMaximum(360)

    def ui_init(self):
        with StyleSheet('slider.css') as style:
            self.setStyleSheet(style)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.__resize_slider(52)

    def __resize_slider(self, percent):
        ps = self.parent().size()
        w = int(ps.width() * percent / 100)
        x = ps.width() // 2 - w // 2
        buttons_g = self.parent().playbutton.geometry()
        y = buttons_g.y()
        self.setGeometry(x, y + buttons_g.height() + 10, w, 12)

    def sliderMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Получение значения слайдера в пиксельных координатах
            pixelValue = event.pos().x()
            # Перевод пиксельных координат в значение слайдера
            sliderValue = self.minimum() + int(pixelValue / self.width() * (self.maximum() - self.minimum()))
            # Установка нового значения слайдера
            self.setValue(sliderValue)
            self.parent().parent().Player.set_pos(sliderValue)

    def sliderEnterEvent(self, event):
        with open("config.json", "r", encoding="utf-8") as style:
            data = json.load(style)
        now = self.styleSheet()
        self.setStyleSheet(now + "QSlider::handle:horizontal { width: 12px; }" +
                           "QSlider::sub-page {background-color:" + data["Theme"] + ";}")

    # Функция, вызываемая при выходе мыши из слайдера
    def sliderLeaveEvent(self, event):
        # Установка стиля для скрытия бегунка при выходе
        now = self.styleSheet()
        self.setStyleSheet(now + "QSlider::handle:horizontal { width: 0px; }" +
                           "QSlider::sub-page {background-color:white;}")


class AddButton(QToolButton):
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
        self.__resize_button(8)
        self.released.connect(self.on_release)

    def __resize_button(self, percent):
        combobox_size = self.parent().combobox.size()
        main_size = self.parent().size()

        w = h = int(main_size.width() * percent / 100)

        self.setGeometry(main_size.width() - combobox_size.width() - 10 - w, 5, w, h)

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
            self.parent().combobox.rewrite()


class DelButton(QToolButton):
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
        self.__resize_button(8)
        self.released.connect(self.on_release)

    def __resize_button(self, percent):
        combobox_size = self.parent().combobox.size()
        main_size = self.parent().size()

        w = h = int(main_size.width() * percent / 100)

        self.setGeometry(main_size.width() - combobox_size.width() - 10 - w, 10 + h, w, h)

    def on_release(self):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        combobox = self.parent().combobox
        try:
            del data["PlayLists"][combobox.currentItem().text()]
        except:
            pass
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        combobox.rewrite()
