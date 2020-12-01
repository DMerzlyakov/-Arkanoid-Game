import pygame as pg
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group
from pygame.font import Font

from settings import WIDTH, HEIGHT


class Score(Sprite):
    """
    Создает объект счета игры
    """
    counter: int = None  # внутренний счетчик
    num: int = None  # кол-во разрядов счетчика
    font: str = None  # путь к файлу с шрифтом
    size: int = None  # размер шрифта
    color: (int, int, int) = None  # цвет шрифта
    text: Font = None  # объект шрифта определнного размера
    image: Surface = None  # поверхность, содержащая текст
    rect: Rect = None  # объект с размерами поверхности

    def __init__(self, font: str, size: int, color: (int, int, int), *groups: Group):
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
        if self.num != len(str(self.counter)):  # масштабирование шрифта при увеличении разрядности счетчика
            self.num = len(str(self.counter))
            size = int(self.size / (self.num / 2))
            self.text = Font(self.font, size)

        self.image = self.text.render(str(self.counter), True, self.color)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)
