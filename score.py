import pygame as pg
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group
from pygame.font import Font

from settings import WIDTH, HEIGHT


class Score(Sprite):
    counter: int = None
    num: int = None
    font: str = None
    size: int = None
    color: tuple[int, int, int] = None
    text: Font = None
    image: Surface = None
    rect: Rect = None

    def __init__(self, font: str, size: int, color: tuple[int, int, int], *groups: Group):
        super(Score, self).__init__(*groups)
        self.counter = 0
        self.num = len(str(self.counter))
        self.font = font
        self.size = size
        self.color = color

        pg.font.init()
        self.text = Font(self.font, self.size)
        self.image = self.text.render(str(self.counter), True, self.color)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    def update(self, num: int):
        self.counter += num
        if self.num != len(str(self.counter)):
            self.num = len(str(self.counter))
            size = int(self.size / (self.num / 2))
            self.text = Font(self.font, size)

        self.image = self.text.render(str(self.counter), True, self.color)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)
