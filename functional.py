from PyQt6.QtCore import QThread, QTimer
import os
import pygame
from pygame.locals import *


class MusicPlayer(QThread):
    playlist = []
    current = 0
    paused = True
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
        except Exception as ex:
            print(ex)

    def set_slider(self):
        slider = self.parent.Player_Frame.musicslider
        sound = pygame.mixer.Sound(self.playlist[self.current])
        duration = sound.get_length()
        slider.setMaximum(int(duration))

    def run(self):
        END_OF_TRACK_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(END_OF_TRACK_EVENT)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == END_OF_TRACK_EVENT:
                    self.next()

    def get_playlist(self, path):
        try:
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
            self.update_slider()
            self.pos = 0
            self.set_slider()
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
            self.update_slider()
            self.pos = 0
            self.set_slider()
        except Exception as ex:
            print(ex)

    def set_pos(self, pos):
        pygame.mixer.music.set_pos(pos)
        self.pos = pos
