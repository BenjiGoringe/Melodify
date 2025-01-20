import pygame

from pathlib import Path

class Music:
    def __init__(self, file: Path):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        self.paused = False

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.stop()

    def unpause(self):
        pygame.mixer.music.unpause()
