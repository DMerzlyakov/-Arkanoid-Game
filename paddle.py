import pygame as pg
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group

from settings import WIDTH


class Paddle(Sprite):
    image: Surface = None
    rect: Rect = None

    def __init__(self, x: float, y: float, width: float, height: float,
                 color: tuple[int, int, int], *groups: Group):

        super(Paddle, self).__init__(*groups)
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width >= WIDTH:
            self.rect.x = WIDTH - self.rect.width

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)
