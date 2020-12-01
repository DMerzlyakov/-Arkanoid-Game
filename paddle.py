import pygame as pg
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group

from settings import WIDTH, PADDlE_SPRITE


class Paddle(Sprite):
    """
    Создает объект платформы
    """
    image: Surface = None  # поверхность, на которой отрисована платформа
    rect: Rect = None  # объект с размерами и координатами поверхности
    sprite: str = PADDlE_SPRITE
    color: (int, int, int) = None  # цвет

    def __init__(self, x: float, y: float, width: float, height: float,
                 color: (int, int, int), *groups: Group):

        super(Paddle, self).__init__(*groups)
        self.color = color
        self.image = pg.transform.scale(pg.image.load(self.sprite), (width, height)).convert()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]  # расположение зависит от положения курсора мыши

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width >= WIDTH:
            self.rect.x = WIDTH - self.rect.width

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)
