import pygame
from gui.text import Text

class LoadingBar:
    def __init__(self, x, y, width, height, progress):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = progress

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.x, self.y, self.width*self.progress, self.height))
        Text(f"{round(self.progress*100, 2)}%", ("Calibri", self.height), (0, 0, 0), (self.x, self.y)).render(screen)