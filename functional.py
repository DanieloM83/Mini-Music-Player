from PyQt6.QtCore import QThread, QTimer
from PyQt6.QtGui import QIcon
import os
import pygame
from pygame.locals import *


class MusicPlayer(QThread):
    playlist = []
    current = 0
    paused = True
    isstop = True
    duration = 0
    pos = 0

    def __init__(self, parent):
        super(MusicPlayer, self).__init__()
        pygame.init()
        self.parent = parent
        timer = QTimer()
        timer.timeout.connect(self.update_slider)
        self.timer = timer
        pygame.mixer.init()

    def update_slider(self):
        try:
            slider = self.parent.Player_Frame.musicslider
            slider.setValue(self.pos)
            self.pos += 1
            self.parent.Player_Frame.set_label(self.format_time(self.pos), self.format_time(self.duration-self.pos))
            if self.pos >= slider.maximum():
                self.next()
        except Exception as ex:
            print(ex)

    def set_slider(self):
        slider = self.parent.Player_Frame.musicslider
        sound = pygame.mixer.Sound(self.playlist[self.current])
        duration = sound.get_length()
        self.duration = duration
        slider.setMaximum(int(duration))

    def run(self):
        ...

    def get_playlist(self, path):
        try:
            self.isstop = False
            extensions = [".mp3", ".wav", ".wma"]

            file_paths = []

            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path) and any(file.endswith(extension) for extension in extensions):
                    file_paths.append(file_path)

            self.playlist = file_paths
            self.current = -1
            self.pos = 0
            self.next()
        except Exception as e:
            print(e)

    def play_stop(self):
        if not self.isstop:
            if self.paused:
                self.paused = False
                pygame.mixer.music.unpause()
                self.timer.start(1000)
            else:
                self.paused = True
                pygame.mixer.music.pause()
                self.timer.stop()

    def next(self):
        try:
            self.pos = 0
            self.current += 1
            if self.current >= len(self.playlist):
                self.current = 0
            pygame.mixer.music.load(self.playlist[self.current])
            pygame.mixer.music.play()
            if self.paused:
                pygame.mixer.music.pause()
            self.pos = 0
            self.set_slider()
            self.update_slider()
        except Exception as ex:
            print(ex)

    def prev(self):
        try:
            self.pos = 0
            self.current -= 1
            if self.current < 0:
                self.current = len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current])
            pygame.mixer.music.play()
            if self.paused:
                pygame.mixer.music.pause()
            self.pos = 0
            self.set_slider()
            self.update_slider()
        except Exception as ex:
            print(ex)

    def set_pos(self, pos):
        pygame.mixer.music.set_pos(pos)
        self.pos = pos

    def set_volume(self, volume):
        volume = volume / 100
        pygame.mixer.music.set_volume(volume)

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"

    def stop(self):
        pygame.mixer.music.stop()
        self.playlist = []
        self.paused = True
        self.isstop = True
        self.timer.stop()
        self.parent.Player_Frame.set_label(self.format_time(0), self.format_time(0))
        self.parent.Player_Frame.playbutton.setIcon(QIcon("style/resources/play.svg"))
        self.parent.Player_Frame.musicslider.setValue(0)