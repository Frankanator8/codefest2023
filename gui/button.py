import pygame

class Button:
    def __init__(self, x, y, width, height, text=None, color=None, image=None, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.callback = callback
        self.text = text
        self.color = color
        self.prevMouseClicked = False

    def render(self, screen):
        if self.color is not None:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height), border_radius=10)

        if self.text is not None:
            self.text.render(screen)

        if self.image is not None:
            screen.blit(self.image, (self.x, self.y))


    def check(self, mouseX, mouseY, mouseClicked):
        if mouseX >= self.x and mouseX <= self.x+self.width and mouseY>=self.y and mouseY<=self.y+self.height:
            if mouseClicked and not self.prevMouseClicked:
                if self.callback is not None:
                    self.callback()

        self.prevMouseClicked = mouseClicked
